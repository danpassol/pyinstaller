# core/runner.py

import subprocess
from core.distro import Distro
from core.logger import setup_logger
from rich.console import Console
from rich.live import Live
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

log = setup_logger()
console = Console()


class CommandRunner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.distro = Distro()
        self.package_manager = self.distro.package_manager

    def _execute(self, cmd):
        if self.verbose:
            console.rule(f"[bold cyan]Running: {cmd}")
            process = subprocess.Popen(cmd, shell=True)
            process.communicate()
            if process.returncode != 0:
                log.error(f"Command failed: {cmd}")
        else:
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode().strip() if result else None

    def _rich_step(self, label, cmd):
        if self.verbose:
            return self._execute(cmd)

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn()
        )

        with Live(progress, console=console, transient=True):
            task_id = progress.add_task(label, start=True)
            try:
                self._execute(cmd)
            except subprocess.CalledProcessError as e:
                progress.stop()
                log.error(e.stderr.decode().strip())
                raise
            finally:
                progress.update(task_id, completed=100)

    def install(self, packages, spinner="dots"):
        desc = f"Installing {', '.join(packages)}"
        cmd = self.distro.install_cmd(packages)
        log.info(desc)
        return self._rich_step(desc, cmd)

    def upgrade(self, spinner="dots"):
        desc = "Upgrading system"
        cmd = self.distro.update_cmd()
        log.info(desc)
        return self._rich_step(desc, cmd)

    def remove(self, packages, spinner="dots"):
        desc = f"Removing {', '.join(packages)}"
        cmd = self.distro.remove_cmd(packages)
        log.info(desc)
        return self._rich_step(desc, cmd)

    def run(self, cmd, capture_output=False):
        return self._execute(cmd)
