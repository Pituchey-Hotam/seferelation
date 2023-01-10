import datetime
from pathlib import Path


TEE = True


log_file = Path(f"logs/{str(datetime.datetime.now())}")
log_file.parent.mkdir(parents=True, exist_ok=True)


def log(message: str):
    if TEE:
        print(message)
    with open(log_file, "a") as f:
        f.write(f"[{str(datetime.datetime.now())}] ")
        f.write(message)
        f.write("\n")

