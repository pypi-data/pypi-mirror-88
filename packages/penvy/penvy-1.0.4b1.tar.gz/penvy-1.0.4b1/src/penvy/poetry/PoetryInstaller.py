import os
import re
import urllib.request
import tempfile
from distutils.version import StrictVersion
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_shell_command, run_and_read_line
from penvy.string.random_string_generator import generate_random_string


class PoetryInstaller(SetupStepInterface):
    def __init__(
        self,
        conda_executable_path: str,
        poetry_executable_path: str,
        install_version: str,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._poetry_executable_path = poetry_executable_path
        self._install_version = install_version
        self._logger = logger

    def get_description(self):
        return f"Install poetry {self._install_version}"

    def run(self):
        self._logger.info("Installing Poetry globally")

        tmp_dir = tempfile.gettempdir()
        target_file_name = tmp_dir + f"/get-poetry_{generate_random_string(5)}.py"

        url = "https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py"
        urllib.request.urlretrieve(url, target_file_name)

        cmd_parts = [self._conda_executable_path, "run", "-n", "base", "python", target_file_name, "-y", "--version", self._install_version]

        run_shell_command(" ".join(cmd_parts), shell=True)

    def should_be_run(self) -> bool:
        return not self._poetry_installed() or not self._poetry_up_to_date()

    def _poetry_installed(self):
        return os.path.isfile(self._poetry_executable_path)

    def _poetry_up_to_date(self):
        current_version = self._get_poetry_version()

        return StrictVersion(current_version) >= StrictVersion(self._install_version)

    def _get_poetry_version(self):
        cmd_parts = [self._conda_executable_path, "run", "-n", "base", "python", self._poetry_executable_path, "-V"]

        first_line = run_and_read_line(" ".join(cmd_parts), shell=True)

        match = re.match(r"^Poetry version ([\d.]+)$", first_line)

        if not match:
            raise Exception(f"Unable to resolve current poetry version. Try updating poetry manually to {self._install_version}")

        return match.group(1)
