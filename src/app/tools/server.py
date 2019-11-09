import sys
import os
import argparse
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "lib"))
import util  # noqa
import encrypted_msg   # noqa

__SERVER_VERSION__ = 0.1


def get_cmd_args():
    global __SERVER_VERSION__
    parser = argparse.ArgumentParser(description="Remote shell server.",
                                     add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-h", "--help", action="help",
                        help="Print this help message and exit.")
    parser.add_argument("-v", "--version", action="version", version=str(
        __SERVER_VERSION__), help="Print the server's version and exit.")
    parser.add_argument(
        "--host", type=str, help="Listening hostname or IPv4 address.", default="0.0.0.0")
    parser.add_argument("--port", type=util.check_positive_arg,
                        help="Listening port number.", default=6969)
    parser.add_argument("--with-password", metavar="PASSWORD",
                        help="Login password.", default=None)
    parser.add_argument("--no-logs", action="store_true",
                        help="Whether or not to print logs.", default=False)
    return parser.parse_args()


def run_server(cmd_args):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((cmd_args.host, cmd_args.port))
    server.listen()
    util.log(util.LOG_TYPE.NORMAL, "Listening on {host}:{port}...".format(
        host=cmd_args.host, port=cmd_args.port), no_logs=cmd_args.no_logs)
    key = encrypted_msg.generate_key()
    while True:
        sock, _ = server.accept()
        recvd_text = encrypted_msg.recv(sock, key)
        util.log(util.LOG_TYPE.NORMAL, "Text recvd:\n\n{recvd_text}".format(
        recvd_text=recvd_text), no_logs=cmd_args.no_logs)
        encrypted_msg.send(sock, recvd_text)


if __name__ == "__main__":
    sys.exit(run_server(get_cmd_args()))
