from logging import Logger
from distutils.version import StrictVersion
from penvy.conda.CondaVersionGetter import CondaVersionGetter
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_shell_command


class DependenciesInstaller(SetupStepInterface):
    def __init__(
        self,
        conda_executable_path: str,
        venv_dir: str,
        poetry_executable_path: str,
        verbose_output_enabled: bool,
        conda_version_getter: CondaVersionGetter,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._venv_dir = venv_dir
        self._poetry_executable_path = poetry_executable_path
        self._verbose_output_enabled = verbose_output_enabled
        self._conda_version_getter = conda_version_getter
        self._logger = logger

    def get_description(self):
        return "Install all python dependencies"

    def run(self):
        self._logger.info("Installing dependencies from poetry.lock")

        conda_version = self._conda_version_getter.get()

        conda_run_parts = [
            self._conda_executable_path,
            "run",
            "-p",
            self._venv_dir,
        ]

        if StrictVersion(conda_version) > StrictVersion("4.9.0"):
            conda_run_parts.append("--no-capture-output")
        else:
            self._logger.warning("Upgrade to Miniconda 4.9.0+ to see live output")

        poetry_install_parts = [
            "python",
            self._poetry_executable_path,
            "install",
            "--no-root",
        ]

        if self._verbose_output_enabled:
            poetry_install_parts.append("-vvv")

        run_shell_command(" ".join(conda_run_parts + poetry_install_parts), shell=True)

    def should_be_run(self) -> bool:
        return True
