from feeder.common import utils

run_id = utils.get_run_id()


def log(message, error=False):
    error_str = "ERROR" if error else "INFO"
    print("[%s] %s: %s" % (run_id, error_str, message))

