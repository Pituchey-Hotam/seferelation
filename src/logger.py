import datetime


TEE = True


log_file = "logs/{str(datetime.datetime.now())}"


def log(message: str):
    if TEE:
        print(message)
    with open(log_file, "a") as f:
        f.write(f"[{str(datetime.datetime.now())}] ")
        f.write(message)
        f.write("\n")

