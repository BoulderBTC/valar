import socket
import json
import logging
import smtplib
from email.mime.text import MIMEText
from valar import valar_settings as settings

class CgminerAPI(object):
    """ Cgminer RPC API wrapper. """
    def __init__(self, host='localhost', port=4028):
        self.data = {}
        self.host = host
        self.port = port

    def command(self, command, arg=None):
        """ Initialize a socket connection,
        send a command (a json encoded dict) and
        receive the response (and decode it).
        """
        payload = {"command": command}
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        try:
            sock.connect((self.host, self.port))
            if arg is not None:
                # Parameter must be converted to basestring (no int)
                payload.update({'parameter': unicode(arg)})

            sock.send(json.dumps(payload))
            received = self._receive(sock)
        except:
            subject = "{0} - ERROR".format(self.host)
            message = "{0} - Error\n\n{1}".format(self.host, "timeout")
            send_mail(subject, message)
        finally:
          #avoid error on OSX
          try:
            sock.shutdown(socket.SHUT_RDWR)
          except socket.error, errno:
            logging.error(str(errno))
          sock.close()

        return json.loads(received[:-1])

    def _receive(self, sock, size=4096):
        msg = ''
        while 1:
            chunk = sock.recv(size)
            if chunk:
                msg += chunk
            else:
                break
        return msg

    def __getattr__(self, attr):
        """ Allow us to make command calling methods.

        >>> cgminer = CgminerAPI()
        >>> cgminer.summary()

        """
        def out(arg=None):
            return self.command(attr, arg)
        return out

def send_mail(subject, message):
    username = settings.gmail_user
    password = settings.gmail_password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    msg = MIMEText(message)
    sender = settings.email_sender
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(settings.toaddrs)
    server.sendmail(sender, settings.toaddrs, msg.as_string())
