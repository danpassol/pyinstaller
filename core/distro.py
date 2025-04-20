# core/distro.py

import os
from core.logger import setup_logger

log = setup_logger()

class Distro:
    def __init__(self):
        self.id = None
        self.version = None
        self.package_manager = None
        self._detect()

    def _detect(self):
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        self.id = line.strip().split("=")[1].strip('"')
                    elif line.startswith("VERSION_ID="):
                        self.version = line.strip().split("=")[1].strip('"')
        else:
            log.error("Unable to detect distribution. Missing /etc/os-release.")
            raise RuntimeError("Unsupported Linux distribution")

        log.info(f"Detected distribution: [bold green]{self.id} {self.version}[/]")
        self._set_package_manager()

    def _set_package_manager(self):
        if self.id in ["ubuntu", "debian"]:
            self.package_manager = "apt"
        elif self.id in ["fedora", "centos", "rhel"]:
            self.package_manager = "dnf"
        elif self.id in ["arch", "manjaro"]:
            self.package_manager = "pacman"
        else:
            log.warning(f"Unknown distribution: {self.id}. Defaulting to [italic]manual[/] mode.")
            self.package_manager = None

    def install_cmd(self, packages):
        if self.package_manager == "apt":
            return f"apt install -y {' '.join(packages)}"
        elif self.package_manager == "dnf":
            return f"dnf install -y {' '.join(packages)}"
        elif self.package_manager == "pacman":
            return f"pacman -S --noconfirm {' '.join(packages)}"
        else:
            log.error("No known package manager for this distribution.")
            return None

    def update_cmd(self):
        if self.package_manager == "apt":
            return "apt update"
        elif self.package_manager == "dnf":
            return "dnf check-update"
        elif self.package_manager == "pacman":
            return "pacman -Sy"
        else:
            return None
