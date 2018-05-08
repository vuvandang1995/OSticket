import logging
import re


class OsTicketFilter(logging.Filter):
    def __init__(self, ip, user, action):
        super(OsTicketFilter, self).__init__()
        self.ip = ip
        self.user = user
        self.action = action

    def filter(self, record):
        record.ip = self.ip
        record.user = self.user
        record.action = self.action
        return True


file_log = logging.FileHandler('osticket.log')
file_log.setFormatter(logging.Formatter('%(asctime)-15s %(name)-10s %(levelname)-8s %(ip)-15s %(user)s %(action)s %(message)s'))

user_log = logging.getLogger('USER_LOG')
user_log.addHandler(file_log)
user_log.setLevel(logging.INFO)

agent_log = logging.getLogger('AGENT_LOG')
agent_log.addHandler(file_log)
agent_log.setLevel(logging.INFO)

ticket_log = logging.getLogger('TICKET_LOG')
ticket_log.addHandler(file_log)
ticket_log.setLevel(logging.INFO)


def write_log(logger, ip, user, action, msg):
    ft = OsTicketFilter(ip=ip, user=user, action=action)
    logger.addFilter(ft)
    logger.info(msg)


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


