import datetime
import json


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__().replace(" ", "T")


def apply(log, output_path, parameters=None):
    if parameters is None:
        parameters = {}

    json.dump(log, open(output_path, "w"), indent=2, default=myconverter)
