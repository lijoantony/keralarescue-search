import datetime

run_id = 0

def get_run_id():
    now = datetime.datetime.now()
    return now.strftime("%m%d_%H%M")

def log(message, error=False):
    error_str = "ERROR" if error else "INFO"
    print("[%s] %s: %s" % (run_id, error_str, message))

