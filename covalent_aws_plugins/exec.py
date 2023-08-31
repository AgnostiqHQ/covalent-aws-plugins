import contextlib
import json
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

io_output_filename = result_filename.rsplit('.', maxsplit=1)[0]
io_output_filename = io_output_filename.replace("result", "io_output") + ".json"

# Create files for function, result, and outputs.
local_func_filename = os.path.join("/covalent", func_filename)
local_result_filename = os.path.join("/covalent", result_filename)
local_io_output_filename = os.path.join("/covalent", io_output_filename)

# Load task function.
s3 = boto3.client("s3")
s3.download_file(s3_bucket, func_filename, local_func_filename)

with open(local_func_filename, "rb") as f_result:
    function, args, kwargs = pickle.load(f_result)


class _TeeStream:

    # Used for tee-ing stdout/stderr with file streams.

    def __init__(self, stream, filename):
        self.streams = (stream, open(filename, "w", encoding="utf-8"))
        self.filename = filename

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def close(self):
        # Close the file stream opened in `__init__`.
        self.streams[1].close()


# Create tee streams to copy stdout/stderr to local files.
stdout_tee = _TeeStream(sys.stdout, os.path.join("/covalent", "stdout.log"))
stderr_tee = _TeeStream(sys.stderr, os.path.join("/covalent", "stderr.log"))

result = None
task_exception = None
traceback_str = None
exception_class_name = None

# Redirect stdout/stderr to tee streams.
with contextlib.redirect_stdout(stdout_tee), contextlib.redirect_stderr(stderr_tee):
    try:
        # RUN TASK FUNCTION
        result = function(*args, **kwargs)

    except Exception as exception:
        # Collect error information.
        task_exception = exception
        traceback_str = traceback.format_exc()
        exception_class_name = exception.__class__.__name__

    finally:
        # Close the log file streams.
        stdout_tee.close()
        stderr_tee.close()

# Create the local outputs file (no pickle for text).
with open(local_io_output_filename, "w", encoding="utf-8") as f_io_output, \
        open(stdout_tee.filename, "r", encoding="utf-8") as f_stdout, \
        open(stderr_tee.filename, "r", encoding="utf-8") as f_stderr:

    stdout = f_stdout.read()
    stderr = f_stderr.read()
    json.dump((stdout, stderr, traceback_str, exception_class_name), f_io_output)

# Upload the local outputs file.
s3.upload_file(local_io_output_filename, s3_bucket, io_output_filename)

if task_exception is not None:
    raise task_exception

# Create the local result file.
with open(local_result_filename, "wb") as f_result:
    pickle.dump(result, f_result)

# Upload the local result file.
s3.upload_file(local_result_filename, s3_bucket, result_filename)
