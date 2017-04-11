import re
import netaddr

from common import utils

LOOPBACK_DEVNAME = 'lo'
GRE_TUNNEL_DEVICE_NAMES = ['gre0', 'gretap0']

SYS_NET_PATH = '/sys/class/net'
DEFAULT_GW_PATTERN = re.compile(r"via (\S+)")
METRIC_PATTERN = re.compile(r"metric (\S+)")
DEVICE_NAME_PATTERN = re.compile(r"(\d+?): (\S+?):.*")

def remove_interface_suffix(interface):
    """Remove a possible "<if>@<endpoint>" suffix from an interface' name.

    This suffix can appear in some kernel versions, and intends on specifying,
    for example, a veth's pair. However, this interface name is useless to us
    as further 'ip' commands require that the suffix be removed.
    """
    # If '@' is not present, this will do nothing.
    return interface.partition("@")[0]

def add_namespace_to_cmd(cmd, namespace=None):
    """Add an optional namespace to the command."""

    return ['ip', 'netns', 'exec', namespace] + cmd if namespace else cmd

class AddressNotReady(Exception):
    message = _("Failure waiting for address %(address)s to "
                "become ready: %(reason)s")

class IpCommandBase(object):
    COMMAND = ''

    def __init__(self, parent):
        self._parent = parent

    def _run(self, options, args):
        return self._parent._run(options, self.COMMAND, args)

    def _as_root(self, options, args, use_root_namespace=False):
        return self._parent._as_root(options,
                                     self.COMMAND,
                                     args,
                                     use_root_namespace=use_root_namespace)

class IpDeviceCommandBase(IpCommandBase):
    @property
    def name(self):
        return self._parent.name

class IpAddrCommand(IpDeviceCommandBase):
    COMMAND = 'addr'

    def add(self, cidr, scope='global', add_broadcast=True):
        net = netaddr.IPNetwork(cidr)
        args = ['add', cidr,
                'scope', scope,
                'dev', self.name]
        if add_broadcast and net.version == 4:
            args += ['brd', str(net[-1])]
        self._as_root([net.version], tuple(args))

    def delete(self, cidr):
        ip_version = utils.get_ip_version(cidr)
        self._as_root([ip_version],
                      ('del', cidr,
                       'dev', self.name))

    def flush(self, ip_version):
        self._as_root([ip_version], ('flush', self.name))

    def get_devices_with_ip(self, name=None, scope=None, to=None,
                            filters=None, ip_version=None):
        """Get a list of all the devices with an IP attached in the namespace.

        @param name: if it's not None, only a device with that matching name
                     will be returned.
        """
        options = [ip_version] if ip_version else []

        args = ['show']
        if name:
            args += [name]
        if filters:
            args += filters
        if scope:
            args += ['scope', scope]
        if to:
            args += ['to', to]

        retval = []

        for line in self._run(options, tuple(args)).split('\n'):
            line = line.strip()

            match = DEVICE_NAME_PATTERN.search(line)
            if match:
                # Found a match for a device name, but its' addresses will
                # only appear in following lines, so we may as well continue.
                device_name = remove_interface_suffix(match.group(2))
                continue
            elif not line.startswith('inet'):
                continue

            parts = line.split(" ")
            if parts[0] == 'inet6':
                scope = parts[3]
            else:
                if parts[2] == 'brd':
                    scope = parts[5]
                else:
                    scope = parts[3]

            retval.append(dict(name=device_name,
                               cidr=parts[1],
                               scope=scope,
                               dynamic=('dynamic' == parts[-1]),
                               tentative=('tentative' in line),
                               dadfailed=('dadfailed' == parts[-1])))
        return retval

    def list(self, scope=None, to=None, filters=None, ip_version=None):
        """Get device details of a device named <self.name>."""
        return self.get_devices_with_ip(
            self.name, scope, to, filters, ip_version)

    def wait_until_address_ready(self, address, wait_time=30):
        """Wait until an address is no longer marked 'tentative'

        raises AddressNotReady if times out or address not present on interface
        """
        def is_address_ready():
            try:
                addr_info = self.list(to=address)[0]
            except IndexError:
                raise AddressNotReady(
                    address=address,
                    reason=_('Address not present on interface'))
            if not addr_info['tentative']:
                return True
            if addr_info['dadfailed']:
                raise AddressNotReady(
                    address=address, reason=_('Duplicate address detected'))
        errmsg = _("Exceeded %s second limit waiting for "
                   "address to leave the tentative state.") % wait_time
        utils.wait_until_true(
            is_address_ready, timeout=wait_time, sleep=0.20,
            exception=AddressNotReady(address=address, reason=errmsg))

class IpCommandBase(object):
    COMMAND = ''

    def __init__(self, parent):
        self._parent = parent

    def _run(self, options, args):
        return self._parent._run(options, self.COMMAND, args)

    def _as_root(self, options, args, use_root_namespace=False):
        return self._parent._as_root(options,
                                     self.COMMAND,
                                     args,
                                     use_root_namespace=use_root_namespace)

class IpLinkCommand(IpDeviceCommandBase):
    COMMAND = 'link'

    def set_address(self, mac_address):
        self._as_root([], ('set', self.name, 'address', mac_address))

    def set_allmulticast_on(self):
        self._as_root([], ('set', self.name, 'allmulticast', 'on'))

    def set_mtu(self, mtu_size):
        self._as_root([], ('set', self.name, 'mtu', mtu_size))

    def set_up(self):
        return self._as_root([], ('set', self.name, 'up'))

    def set_down(self):
        return self._as_root([], ('set', self.name, 'down'))

    def set_netns(self, namespace):
        self._as_root([], ('set', self.name, 'netns', namespace))
        self._parent.namespace = namespace

    def set_name(self, name):
        self._as_root([], ('set', self.name, 'name', name))
        self._parent.name = name

    def set_alias(self, alias_name):
        self._as_root([], ('set', self.name, 'alias', alias_name))

    def delete(self):
        self._as_root([], ('delete', self.name))

    @property
    def address(self):
        return self.attributes.get('link/ether')

    @property
    def state(self):
        return self.attributes.get('state')

    @property
    def mtu(self):
        return self.attributes.get('mtu')

    @property
    def qdisc(self):
        return self.attributes.get('qdisc')

    @property
    def qlen(self):
        return self.attributes.get('qlen')

    @property
    def alias(self):
        return self.attributes.get('alias')

    @property
    def attributes(self):
        return self._parse_line(self._run(['o'], ('show', self.name)))

    def _parse_line(self, value):
        if not value:
            return {}

        device_name, settings = value.replace("\\", '').split('>', 1)
        tokens = settings.split()
        keys = tokens[::2]
        values = [int(v) if v.isdigit() else v for v in tokens[1::2]]

        retval = dict(zip(keys, values))
        return retval

class SubProcessBase(object):
    def __init__(self, namespace=None,
                 log_fail_as_error=True):
        self.namespace = namespace
        self.log_fail_as_error = log_fail_as_error
        self.force_root = False

    def _run(self, options, command, args):
        if self.namespace:
            return self._as_root(options, command, args)
        elif self.force_root:
            # Force use of the root helper to ensure that commands
            # will execute in dom0 when running under XenServer/XCP.
            return self._execute(options, command, args, run_as_root=True,
                                 log_fail_as_error=self.log_fail_as_error)
        else:
            return self._execute(options, command, args,
                                 log_fail_as_error=self.log_fail_as_error)

    def _as_root(self, options, command, args, use_root_namespace=False):
        namespace = self.namespace if not use_root_namespace else None

        return self._execute(options, command, args, run_as_root=True,
                             namespace=namespace,
                             log_fail_as_error=self.log_fail_as_error)

    @classmethod
    def _execute(cls, options, command, args, run_as_root=False,
                 namespace=None, log_fail_as_error=True):
        opt_list = ['-%s' % o for o in options]
        ip_cmd = add_namespace_to_cmd(['ip'], namespace)
        cmd = ip_cmd + opt_list + [command] + list(args)
        return utils.execute(cmd, run_as_root=run_as_root,
                             log_fail_as_error=log_fail_as_error)

    def set_log_fail_as_error(self, fail_with_error):
        self.log_fail_as_error = fail_with_error

    def get_log_fail_as_error(self):
        return self.log_fail_as_error