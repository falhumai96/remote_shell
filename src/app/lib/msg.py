import socket


def send(sock, text, timeout=60):
    original_timeout = sock.gettimeout()
    if text is None:
        return False
    try:
        sock.settimeout(60)
        text_to_send = "{textlen}~{text}".format(textlen=len(text), text=text)
        sock.send(text_to_send.encode())
        sock.settimeout(original_timeout)
        return True
    except (ConnectionResetError, socket.timeout):
        sock.settimeout(original_timeout)
        return False


def recv(sock, timeout=60):
    original_timeout = sock.gettimeout()
    try:
        sock.settimeout(timeout)
        textlen_str = ''
        curr_char = ''
        while True:
            curr_char = sock.recv(1).decode('utf8')
            if curr_char == '~':
                break
            textlen_str += curr_char

        textlen = int(textlen_str)

        text = ''
        i = 0
        while i < textlen:
            curr_char = sock.recv(1).decode('utf8')
            text += curr_char
            i += 1
        sock.settimeout(original_timeout)
        return text
    except (ConnectionResetError, socket.timeout, ValueError):
        sock.settimeout(original_timeout)
        return None
