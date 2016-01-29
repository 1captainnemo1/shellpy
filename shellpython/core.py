import os
import sys
import subprocess


class Result:
    """Result of a shell command execution.

    To get the result as string use str(Result)
    To get lines use the Result.lines field
    You can also iterate over lines of result like this: for line in Result:
    You can compaire two results that will mean compaire of result strings
    """
    def __init__(self):
        self.stdout_lines = []
        self.stderr_lines = []
        self.returncode = -1

    def stdout_text(self):
        return os.linesep.join(self.stdout_lines)

    def stderr_text(self):
        return os.linesep.join(self.stderr_lines)

    def add_stdout_line(self, line):
        line_no_linesep = line[:-1] if len(line) > 0 and line[-1] == os.linesep else line
        self.stdout_lines.append(line_no_linesep)

    def add_stderr_line(self, line):
        line_no_linesep = line[:-1] if len(line) > 0 and line[-1] == os.linesep else line
        self.stderr_lines.append(line_no_linesep)

    def __str__(self):
        return self.stdout_text()

    def __iter__(self):
        return iter(self.stdout_lines)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __bool__(self):
        return self.returncode == 0

    __nonzero__ = __bool__


def exe(cmd, params):
    """Executes command in shell and returns Result of execution

    :param cmd: Command to execute
    :return: Result of execution
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result = Result()

    for line in p.stdout.readlines():
        if sys.version_info[0] == 3:
            line = line.decode(sys.stdout.encoding)

        result.add_stdout_line(line)

    for line in p.stderr.readlines():
        if sys.version_info[0] == 3:
            line = line.decode(sys.stderr.encoding)

        result.add_stderr_line(line)

    p.wait()

    if params.find('p') != -1:
        print(result.stdout_text())

    if params.find('e') != -1:
        print(result.stderr_text())

    result.returncode = p.returncode

    return result
