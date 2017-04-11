import logging

from common.utils import execute

LOG = logging.getLogger(__name__)

class IpLinkSupportError(Exception):
    pass

class UnsupportedIpLinkCommand(IpLinkSupportError):
    message = "ip link command is not supported: %(reason)s"

class IpLinkSupport(object):
    @classmethod
    def _get_ip_link_output(cls):
        try:
            ip_cmd = ['ls', 'link', 'help']
            _stdout, _stderr = execute(
                ip_cmd,
                check_exit_code=True,
                return_stderr=True,
                log_fail_as_error=False)
        except Exception as e:
            LOG.exception("Failed to execute ip command")
            raise UnsupportedIpLinkCommand
        return _stdout or _stderr



