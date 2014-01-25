import socket
from valar.utils import hosts, send_mail
from valar.pycgm import CgminerAPI


if __name__ == '__main__':
    result = False
    for h in hosts:
        print h, "\n"
        try:
            cgm = CgminerAPI(host=h)
            result = cgm.summary()
        except socket.error as e:
            subject = "{0} - ERROR".format(h)
            message = "{0} - Error\n\n{1}".format(h, e)
            send_mail(subject, message)
        print result
