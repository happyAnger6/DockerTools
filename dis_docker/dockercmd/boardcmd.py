class BoardCmdBase(object):
    def __init__(self, board):
        self._board = board

class DockerBoardCmd(BoardCmdBase):
    def run(self, image, env=[], name=None):
        envcmd = []
        for e in env:
            envcmd += ['-e'] + [e]
        name = name if name else self._board.name
        namecmd = ['--name', name]
        pass

    def start(self, options, args):
        pass

    def stop(self, options, args):
        pass
