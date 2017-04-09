import six

import subprocess

def safe_decode_utf8(s):
    """Safe decode a str from UTF.

    :param s: The str to decode.
    :returns: The decoded str.
    """
    if six.PY3 and isinstance(s, bytes):
        return s.decode('utf-8', 'surrogateescape')
    return s

def addl_env_args(addl_env):
    if addl_env is None:
        return []
    return ['env'] + ['%s=%s'%pair for pair in addl_env.items()]

def create_process(cmd, process_input=None,
                run_as_root=False, addl_env=None):
    cmd = list(map(str, addl_env_args(addl_env) + cmd))
    if run_as_root:
        cmd = "sudo" + cmd
    obj = subprocess.Popen(cmd, shell=False,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    return obj, cmd

def execute(cmd, process_input=None, addl_env=None,
            check_exit_code=True, return_stderr=False, log_fail_as_error=True,
            extra_ok_codes=None, run_as_root=False):
    try:
        if process_input is not None:
            _process_input = process_input.encode('UTF-8')
        else:
            _process_input = None
        obj, cmd = create_process(cmd, run_as_root=run_as_root,
                                  addl_env=addl_env)
        _stdout, _stderr = obj.communicate(_process_input)
        obj.stdin.close()
        _stdout = safe_decode_utf8(_stdout)
        _stderr = safe_decode_utf8(_stderr)
    finally:
        return _stdout, _stderr if return_stderr else _stdout

