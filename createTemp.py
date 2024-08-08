import os
import tempfile

def create_iterate_logs_folder():
    temp_dir = tempfile.gettempdir()
    iterate_logs_path = os.path.join(temp_dir, 'iterateLogs')
    os.makedirs(iterate_logs_path, exist_ok=True)
    print(f"Created or verified directory: {iterate_logs_path}", flush=True)
    return iterate_logs_path

