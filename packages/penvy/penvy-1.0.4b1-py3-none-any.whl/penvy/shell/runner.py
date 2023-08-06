import io
import os
import subprocess


def run_and_read_line(command: str, shell=False):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
    return io.TextIOWrapper(proc.stdout, encoding="utf-8").read().replace("\n", "")


def run_shell_command(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, shell=shell)
    proc.communicate()
