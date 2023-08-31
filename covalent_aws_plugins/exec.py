import contextlib
import os
import sys
import traceback

import boto3
import cloudpickle as pickle


s3_bucket = os.environ["S3_BUCKET_NAME"]
if not s3_bucket:
    raise ValueError("Environment variable S3_BUCKET_NAME was not found")

func_filename = os.environ["COVALENT_TASK_FUNC_FILENAME"]
if not func_filename:
    raise ValueError("Environment variable FUNC_FILENAME was not found")

result_filename = os.environ["RESULT_FILENAME"]
if not result_filename:
    raise ValueError("Environment variable RESULT_FILENAME was not found")

io_output_filename = result_filename.replace("result", "output")

# Create files for function, result, and outputs.
local_func_filename = os.path.join("/covalent", func_filename)
local_result_filename = os.path.join("/covalent", result_filename)
local_io_output_filename = os.path.join("/covalent", io_output_filename)

# Load task function.
s3 = boto3.client("s3")
s3.download_file(s3_bucket, func_filename, local_func_filename)

with open(local_func_filename, "rb") as f:
    function, args, kwargs = pickle.load(f)


class _TeeStream:

    # Used for tee-ing stdout/stderr with file streams.

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()


# Create tee streams to copy stdout/stderr to local files.
stdout_log = os.path.join("/covalent", "stdout.log")
stderr_log = os.path.join("/covalent", "stderr.log")
stdout_tee = _TeeStream(sys.stdout, open(stdout_log, "w", encoding="utf-8"))
stderr_tee = _TeeStream(sys.stderr, open(stderr_log, "w", encoding="utf-8"))

result = None
task_exception = None
traceback_str = None
exception_cls = None

# Redirect stdout/stderr to tee streams.
with contextlib.redirect_stdout(stdout_tee), contextlib.redirect_stderr(stderr_tee):
    try:
        # RUN TASK FUNCTION
        result = function(*args, **kwargs)

    except Exception as exception:
        # Collect error information.
        task_exception = exception
        traceback_str = traceback.format_exc()
        exception_cls = type(exception)

    finally:
        # Close the log file streams.
        stdout_tee.streams[1].close()
        stderr_tee.streams[1].close()

# Create the local outputs file.
with open(local_io_output_filename, "wb") as f, \
        open(stdout_log, "r", encoding="utf-8") as f_out, \
        open(stderr_log, "r", encoding="utf-8") as f_err:

    stdout = f_out.read()
    stderr = f_err.read()
    pickle.dump((stdout, stderr, traceback_str, exception_cls), f)

# Upload the local outputs file.
s3.upload_file(local_io_output_filename, s3_bucket, io_output_filename)

if task_exception is not None:
    raise task_exception

# Create the local result file.
with open(local_result_filename, "wb") as f:
    pickle.dump(result, f)

# Upload the local result file.
s3.upload_file(local_result_filename, s3_bucket, result_filename)
