from contextlib import redirect_stdout, redirect_stderr
import io
import json
import os
import sys
import traceback
from typing import Any, Callable, Dict, List, Tuple

import boto3
import cloudpickle as pickle

from covalent._shared_files.qelectron_utils import get_qelectron_db_path
from covalent._workflow.depsbash import DepsBash
from covalent._workflow.depscall import RESERVED_RETVAL_KEY__FILES, DepsCall
from covalent._workflow.depspip import DepsPip
from covalent._workflow.transport import TransportableObject

from covalent.executor.utils.wrappers import _gather_deps, wrapper_fn
from covalent.executor.utils import set_context
from covalent.executor.utils.serialize import deserialize_node_asset, serialize_node_asset


s3_client = boto3.client("s3")

S3_PREFIX = "s3://"
PREFIX_LEN = len(S3_PREFIX)


def _download_from_uri(s3_uri: str) -> bytes:
    if not s3_uri.startswith(S3_PREFIX):
        raise RuntimeError(f"Invalid URI {s3_uri}")
    bucket, key = s3_uri[PREFIX_LEN:].split("/", maxsplit=1)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    return resp["Body"].read()


def _upload_to_uri(data: bytes, s3_uri: str):
    if not s3_uri.startswith(S3_PREFIX):
        raise RuntimeError(f"Invalid URI {s3_uri}")
    bucket, key = s3_uri[PREFIX_LEN:].split("/", maxsplit=1)
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)


def run_task_group(
    task_specs: List[Dict],
    resources: Dict,
    output_uris: List[Tuple[str, str, str, str]],
    summary_uris: List[str],
    task_group_metadata: dict,
):
    """
    This is appropriate for backends that cannot reach the Covalent
    server. Covalent will push input assets to the executor's
    persistent storage before invoking `Executor.send()` and pull output
    artifacts after `Executor.receive()`.

    Example: DaskExecutor.

    """

    outputs = {}

    # Track electrons that tried to run
    results = []

    dispatch_id = task_group_metadata["dispatch_id"]
    task_ids = task_group_metadata["node_ids"]

    os.environ["COVALENT_DISPATCH_ID"] = dispatch_id
    for i, task in enumerate(task_specs):
        result_uri, stdout_uri, stderr_uri, qelectron_db_uri = output_uris[i]
        summary_uri = summary_uris[i]

        # Setting these to empty bytes in case the task fails
        qelectron_db_bytes = bytes()

        with redirect_stdout(io.StringIO()) as stdout, redirect_stderr(io.StringIO()) as stderr:
            try:
                task_id = task["function_id"]
                args_ids = task["args_ids"]
                kwargs_ids = task["kwargs_ids"]

                # Load function
                function_uri = resources["functions"][str(task_id)]

                # Download from S3
                serialized_fn = deserialize_node_asset(_download_from_uri(function_uri), "function")

                # Load args and kwargs
                ser_args = []
                ser_kwargs = {}

                args_uris = [resources["inputs"][str(index)] for index in args_ids]
                for uri in args_uris:
                    # Download from S3
                    ser_args.append(deserialize_node_asset(_download_from_uri(uri), "output"))

                kwargs_uris = {k: resources["inputs"][str(v)] for k, v in kwargs_ids.items()}
                for key, uri in kwargs_uris.items():
                    # Download from S3
                    ser_kwargs[key] = deserialize_node_asset(_download_from_uri(uri), "output")

                # Load deps
                hooks_uri = resources["hooks"][task_id]
                # Download from S3
                hooks_json = deserialize_node_asset(_download_from_uri(hooks_uri), "hooks")

                deps_json = hooks_json.get("deps", {})
                call_before_json = hooks_json.get("call_before", [])
                call_after_json = hooks_json.get("call_after", [])

                # Assemble and invoke the task
                call_before, call_after = _gather_deps(
                    deps_json, call_before_json, call_after_json
                )

                exception_occurred = False

                # Run the task function
                with set_context(dispatch_id, task_id):
                    transportable_output = wrapper_fn(
                        serialized_fn, call_before, call_after, *ser_args, **ser_kwargs
                    )

                ser_output = serialize_node_asset(transportable_output, "output")
                output_size = len(ser_output)

                # Save output
                # Upload to S3
                _upload_to_uri(ser_output, result_uri)

                # Save QElectron DB
                qelectron_db_path = get_qelectron_db_path(dispatch_id, task_id)
                if qelectron_db_path is not None:
                    with open(qelectron_db_path / "data.mdb", "rb") as f:
                        qelectron_db_bytes = f.read()
                # Upload to S3
                _upload_to_uri(qelectron_db_bytes, qelectron_db_uri)

                resources["inputs"][str(task_id)] = result_uri

                qelectron_db_size = len(qelectron_db_bytes)

            except Exception as ex:
                exception_occurred = True
                result_uri = ""
                output_size = 0
                qelectron_db_uri = ""
                qelectron_db_size = 0
                tb = "".join(traceback.TracebackException.from_exception(ex).format())
                print(tb, file=sys.stderr)
                break

            finally:
                stdout.flush()
                stderr.flush()
                stdout_size = os.path.getsize(stdout_uri)
                stderr_size = os.path.getsize(stderr_uri)

                result_summary = {
                    "node_id": task_id,
                    "output": {
                        "uri": result_uri,
                        "size": output_size,
                    },
                    "stdout": {
                        "uri": stdout_uri,
                        "size": stdout_size,
                    },
                    "stderr": {
                        "uri": stderr_uri,
                        "size": stderr_size,
                    },
                    "qelectron_db": {
                        "uri": qelectron_db_uri,
                        "size": qelectron_db_size,
                    },
                    "exception_occurred": exception_occurred,
                }

                result_summary = {
                    "node_id": task_id,
                    "output_uri": result_uri,
                    "stdout_uri": stdout_uri,
                    "stderr_uri": stderr_uri,
                    "qelectron_db_uri": qelectron_db_uri,
                    "exception_occurred": exception_occurred,
                }

                results.append(result_summary)

                # Upload stdout, stderr, and the summary file

                _upload_to_uri(stdout.getvalue().encode("utf-8"), stdout_uri)
                _upload_to_uri(stderr.getvalue().encode("utf-8"), stderr_uri)

                # Write the summary file containing the URIs for
                # the serialized result, stdout, stderr, and qelectron_db
                _upload_to_uri(json.dumps(result_summary).encode("utf-8"), summary_uri)

    # Deal with any tasks that did not run
    n = len(results)
    if n < len(task_ids):
        for i in range(n, len(task_ids)):
            result_summary = {
                "node_id": task_ids[i],
                "output_uri": "",
                "stdout_uri": "",
                "stderr_uri": "",
                "qelectron_db_uri": "",
                "exception_occurred": True,
            }

            results.append(result_summary)
            _upload_to_uri(json.dumps(result_summary).encode("utf-8"), summary_uri)


def main():
    task_specs = json.loads(os.environ["COVALENT_TASK_SPECS"])
    resource_map = json.loads(os.environ["COVALENT_RESOURCE_MAP"])
    output_uris = json.loads(os.environ["COVALENT_OUTPUT_UPLOAD_URIS"])
    task_group_metadata = json.loads(os.environ["COVALENT_TASK_GROUP_METADATA"])
    summary_uris = json.loads(os.environ["COVALENT_SUMMARY_UPLOAD_URIS"])
    run_task_group(task_specs, resource_map, output_uris, summary_uris, task_group_metadata)


if __name__ == "__main__":
    main()
