import time
import json

from framl.config_model import ConfigModel

class Logger:
    MESSAGE_VERSION = 1
    MESSAGE_DEBUG = "debug"
    MESSAGE_INFO = "info"

    def __init__(self, app_path: str):
        model_conf_ob = ConfigModel(app_path)

        self._model_name = model_conf_ob.get_model_name()
        self._model_version = model_conf_ob.get_model_version()
        self._split_debug = model_conf_ob.get_split_log_debug()

    def add(self, prediction_id: str, model_input: dict, model_output: dict, latency: int):
        full_log = {
            "request_latency_in_ms": latency,
            "prediction_id":         prediction_id,
            "message_version":       self.MESSAGE_VERSION,
            "log_type": self.MESSAGE_DEBUG,
            "prediction_time":       int(time.time()),
            "metadata":              {
                "model_name":    self._model_name,
                "model_version": self._model_version,
            },
            "input":                 {**model_input},
            "output":                {**model_output}
        }

        print(json.dumps(full_log))

        if self._split_debug:
            # Keep a separate copy of the output so that it can persist longer.
            full_log.pop("input")
            full_log["message_version"] = self.MESSAGE_INFO
            print(json.dumps(full_log))
