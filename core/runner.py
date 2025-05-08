# core/runner.py

import subprocess
from core.distro import Distro
from core.logger import setup_logger
from rich.console import Console

log = setup_logger()
console = Console()

class CommandRunner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.distro = Distro()  # Uses the singleton instance
        self.package_manager = self.distro.package_manager

    def _run_cmd(self, cmd, capture_output=False, spinner=None, description="Processing command..."):
        try:
            if self.verbose:
                process = subprocess.Popen(cmd, shell=True)
                process.communicate()
                if process.returncode != 0:
                    log.error(f"Command failed: {cmd}")
                return None

            if spinner:
                with console.status(f"[bold green]{description}", spinner=spinner):
                    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if capture_output:
                return result.stdout.decode().strip()
            return None

        except subprocess.CalledProcessError as e:
            log.error(f"Command failed: {cmd}")
            log.error(f"Error message: {e.stderr.decode().strip()}")
            raise e
        
    def install(self, packages, spinner="dots",):
        cmd = self.distro.install_cmd(packages)
        log.info(f"Installing packages: {packages}")
        return self._run_cmd(cmd, spinner=spinner, description="Installing...")

    def upgrade(self, spinner="dots",):
        cmd = self.distro.update_cmd()
        log.info("Upgrading system...")
        return self._run_cmd(cmd, spinner=spinner, description="Updating...")

    def remove(self, packages, spinner="dots",):
        cmd = self.distro.remove_cmd(packages)
        log.info(f"Removing packages: {packages}")
        return self._run_cmd(cmd, spinner=spinner, description="Removing...")

    def run(self, cmd, capture_output=False, spinner=None):
        return self._run_cmd(cmd, capture_output, spinner=spinner, description=None)
