
class DockerCmdBase(object):
    COMMAND = ''

    def __init__(self, parent):
        self.parent = parent

class RunCmd(DockerCmdBase):
    def __init__(self):
        self.cmd = ['docker', 'run']

    def add_name(self, name):
        self.cmd = self.cmd + ['--name', name]

    def add_env(self, env):
        self.cmd = self.cmd + ['--env', env]

    def run(self):
        pass

class StartCmd(DockerCmdBase):
    def __init__(self):
        cmd = ['docker', 'start']

    def run(self):
        pass

if __name__ == "__main__":
    cmd = RunCmd()
    cmd.add_env(['a=1','b=3'])
    print(cmd.cmd)