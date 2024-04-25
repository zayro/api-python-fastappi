from datetime import datetime
import logging
from icecream import ic

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


def output_function(text):
    with open("app.log", "a") as f:
        f.write(text + "\n")


def time_format():
    now = datetime.now()
    return f' log | {now.strftime("%H:%M:%S")} --> '


ic.configureOutput(
    prefix=time_format,
    includeContext=True,
    contextAbsPath=True,
    ## outputFunction=output_function,
)
