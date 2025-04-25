# core/runner.py

import subprocess
from core.distro import Distro
from core.logger import setup_logger

log = setup_logger()

class CommandRunner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.distro = Distro()  # Uses the singleton instance
        self.package_manager = self.distro.package_manager

    def _run_cmd(self, cmd, capture_output=False):
        try:
            if self.verbose:
                process = subprocess.Popen(cmd, shell=True)
                process.communicate()
                if process.returncode != 0:
                    log.error(f"Command failed: {cmd}")
                return None
            else:
                result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if capture_output:
                    return result.stdout.decode().strip()
                return None
        except subprocess.CalledProcessError as e:
            log.error(f"Command failed: {cmd}")
            log.error(f"Error message: {e.stderr.decode().strip()}")
            raise e
        
    def install(self, packages):
        cmd = self.distro.install_cmd(packages)
        log.info(f"Installing packages: {packages}")
        return self._run_cmd(cmd)

    def upgrade(self):
        cmd = self.distro.update_cmd()
        log.info("Upgrading system...")
        return self._run_cmd(cmd)

    def remove(self, packages):
        cmd = self.distro.remove_cmd(packages)
        log.info(f"Removing packages: {packages}")
        return self._run_cmd(cmd)

    def run(self, cmd, capture_output=False):
        return self._run_cmd(cmd, capture_output)
