from common import utils

class SubProcessBase(object):
    def __init__(self, namespace=None,
                 log_fail_as_error=True):
        self.namespace = namespace
        self.log_fail_as_error = log_fail_as_error
        self.force_root = False
        # Only callers that need to force use of the root helper
        # need to register the option.
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
    def _execute(cls, options, command, args, run_as_root=True,
                 namespace=None, log_fail_as_error=True):
        opt_list = ['-%s' % o for o in options]
        docker_cmd = ['docker']
        cmd = docker_cmd + [command] + opt_list + list(args)
        return utils.execute(cmd, run_as_root=run_as_root,
                             log_fail_as_error=log_fail_as_error)

    def set_log_fail_as_error(self, fail_with_error):
        self.log_fail_as_error = fail_with_error

    def get_log_fail_as_error(self):
        return self.log_fail_as_error

class DockerCmdBase(object):
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

class DockerBoardRunCmd(DockerCmdBase):
    COMMAND = 'run'

    def execute(self, board, image, env=[], name=None, entry=None):
        envcmd = []
        for e in env:
            envcmd += ['-e'] + [e]
        name = name if name else board.name
        namecmd = ['--name', name]
        imagecmd = [image]
        args = envcmd + namecmd + imagecmd
        args = args + [entry] if entry else args
        self._as_root(['dt'], args)


