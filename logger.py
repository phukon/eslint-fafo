import os
import json
import requests
import gzip
from threading import Event
from datetime import datetime
from queue import Queue, Empty
from contextvars import ContextVar
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor

message_id_var = ContextVar("message_id", default=None)


class CustomLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_endpoint="http://localhost:5000/logs", max_queue_size=1000, batch_size=100):
        if not hasattr(self, "initialized"):
            self.api_endpoint = api_endpoint
            self.log_queue = Queue(maxsize=max_queue_size)
            self.batch_size = batch_size
            self.stop_event = Event()
            self.executor = ThreadPoolExecutor(max_workers=1)
            self.executor.submit(self._send_logs_worker)
            self.initialized = True

    def _format_log(self, level, message, extra=None):
        log_entry = {
            "level": level,
            "message": message,
            "message_id": message_id_var.get(),
            "timestamp": datetime.utcnow().isoformat() 
        }
        if extra:
            log_entry["extra"] = extra
        return json.dumps(log_entry)

    def debug(self, message, extra=None):
        self._add_to_queue("DEBUG", message, extra)

    def info(self, message, extra=None):
        self._add_to_queue("INFO", message, extra)

    def warning(self, message, extra=None):
        self._add_to_queue("WARNING", message, extra)

    def error(self, message, extra=None):
        self._add_to_queue("ERROR", message, extra)

    def silent(self, message, extra=None):
        self._add_to_queue("INFO", message, extra)

    def _add_to_queue(self, level, message, extra=None):
        log_entry = self._format_log(level, message, extra)

        if level != "DEBUG" and level != "SILENT" or os.getenv("DEBUG_LOGS", "false").lower() == "true":
            print(f"{level}: {message}")

        # Only add non-DEBUG logs to the queue
        if level != "DEBUG":
            try:
                self.log_queue.put_nowait(log_entry)
            except Queue.Full:
                print(f"Warning: Log queue is full. Discarding log: {log_entry}")

    def _send_logs_worker(self):
        while not self.stop_event.is_set():
            batch = []
            for _ in range(self.batch_size):
                try:
                    log_entry = self.log_queue.get(block=True, timeout=1)
                    batch.append(log_entry)
                except Empty:
                    break

            if batch:
                self._send_logs_to_api(batch)

        # Process any remaining logs after stop event is set
        while not self.log_queue.empty():
            batch = []
            while not self.log_queue.empty() and len(batch) < self.batch_size:
                log_entry = self.log_queue.get_nowait()
                batch.append(log_entry)
            if batch:
                self._send_logs_to_api(batch)

    def _send_logs_to_api(self, logs):
        try:
            compressed_logs = gzip.compress(json.dumps(logs).encode("utf-8"))
            headers = {"Content-Encoding": "gzip", "Content-Type": "application/json"}
            response = requests.post(self.api_endpoint, data=compressed_logs, headers=headers)
            if response.status_code != 200:
                print(f"Failed to send logs to API. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending logs to API: {str(e)}")

    # To stop the worker thread and process any remaining messages
    def flush(self):
        self.stop_event.set()  # Signal the worker to stop
        self.executor.shutdown(wait=True)
        self._send_logs_worker()  # Process any remaining logs


@contextmanager
def log_context(message_id):
    token = message_id_var.set(message_id)
    try:
        yield
    finally:
        message_id_var.reset(token)


logger = CustomLogger()


def get_logger():
    return logger