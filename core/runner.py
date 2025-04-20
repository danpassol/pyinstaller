# core/runner.py

import subprocess
from core.distro import Distro
from core.logger import setup_logger

log = setup_logger()

class CommandRunner:
    def __init__(self):
        self.distro = Distro()
        self.package_manager = self.distro.package_manager

    def _run_cmd(self, cmd, capture_output=False):
        """Helper function to run shell commands."""
        try:
            result = subprocess.run(
                cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if capture_output:
                return result.stdout.decode().strip()
            return None
        except subprocess.CalledProcessError as e:
            log.error(f"Command failed: {cmd}")
            log.error(f"Error: {e.stderr.decode().strip()}")
            return None

    def install(self, packages):
        """Install packages using the system's package manager."""
        if not packages:
            log.error("No packages to install.")
            return

        cmd = self.distro.install_cmd(packages)
        log.info(f"Running install command: {cmd}")
        return self._run_cmd(cmd)

    def upgrade(self):
        """Upgrade system packages."""
        cmd = self.distro.update_cmd()
        log.info(f"Running upgrade command: {cmd}")
        return self._run_cmd(cmd)

    def remove(self, packages):
        """Remove packages using the system's package manager."""
        if not packages:
            log.error("No packages to remove.")
            return

        if self.package_manager == "apt":
            cmd = f"apt remove -y {' '.join(packages)}"
        elif self.package_manager == "dnf":
            cmd = f"dnf remove -y {' '.join(packages)}"
        elif self.package_manager == "pacman":
            cmd = f"pacman -R --noconfirm {' '.join(packages)}"
        else:
            log.error(f"Unsupported package manager: {self.package_manager}")
            return None

        log.info(f"Running remove command: {cmd}")
        return self._run_cmd(cmd)

    def run(self, cmd, capture_output=False):
        """Run any command."""
        log.info(f"Running command: {cmd}")
        return self._run_cmd(cmd, capture_output)
