import argparse
import termcolor
import colorama


def check_positive_arg(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                "Expected \"unsigned int\". Found: \"{type}\".".format(type=type(ivalue).__name__))
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Expected \"unsigned int\". Found: \"{type}\".".format(type=type(value).__name__))
    return ivalue


class LOG_TYPE:
    NORMAL = {
        "pretext": "LOG",
        "color": "green"
    }
    WARN = {
        "pretext": "WARN",
        "color": "yellow"
    }
    FATAL = {
        "pretext": "FATAL",
        "color": "red"
    }


def log(log_type, text, no_logs=False):
    colorama.init()
    if not no_logs:
        print(termcolor.colored("{pretext}: {text}".format(
            pretext=log_type["pretext"], text=text), log_type["color"]))
