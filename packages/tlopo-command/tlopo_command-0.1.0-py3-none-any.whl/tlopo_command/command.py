import subprocess
import logging
import shutil

logger = logging.getLogger('tlopo_command.Command')

class Command:
    def __init__(self,command, live=False, must_succeed=False):
        validate_command(command)
        self.command = command
        self.live = live
        self.must_succeed = must_succeed
        self.stdout = ''

    def run(self):
        if hasattr(self, 'returncode'):
            raise Exception('CMD object cannot be reused.')

        logger.debug('Running CMD: [{}]'.format(self.command) )

        if self.live:
            self.returncode = subprocess.run(command_as_list(self.command)).returncode
        else:
            result = subprocess.run(command_as_list(self.command), stdout=subprocess.PIPE)
            self.returncode = result.returncode
            self.stdout = result.stdout.decode('utf-8')

        if self.must_succeed and self.returncode:
            raise Exception(f'Failed to run command: {command_as_list(self.command)}')

        return self


def shell():
    shell = shutil.which('bash')
    if not shell:
        shell = shutil.which('sh')
    if not shell:
        raise Exception('Could not find bash nor sh')
    return shell

def command_as_list(cmd):
    if isinstance(cmd, list):
        return cmd
    elif isinstance(cmd, str):
        return [ shell(), '-c', cmd ]
        

def validate_command(cmd):
    if isinstance(cmd, str):
        return
    elif isinstance(cmd, list) and all(list(map(lambda e: isinstance(e, str), cmd))):
        return
    else:
        raise Exception(f'Type error, command should either string or list of strings')
