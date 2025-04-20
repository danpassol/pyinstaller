# core/distro.py

import os

class Distro:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Distro, cls).__new__(cls)
            cls._instance._detect()
        return cls._instance

    def _detect(self):
        self.id = None
        self.version_codename = None
        self.package_manager = None

        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                data = f.read()
            for line in data.splitlines():
                if line.startswith("ID="):
                    self.id = line.split("=")[1].strip().strip('"')
                elif line.startswith("VERSION_CODENAME="):
                    self.version_codename = line.split("=")[1].strip().strip('"')

        if self.id in ["ubuntu", "debian"]:
            self.package_manager = "apt"
        elif self.id in ["rhel", "fedora", "centos"]:
            self.package_manager = "dnf"
        elif self.id in ["arch"]:
            self.package_manager = "pacman"
        else:
            raise Exception(f"Unsupported distro: {self.id}")

    def install_cmd(self, packages):
        if self.package_manager == "apt":
            return f"apt install -y {' '.join(packages)}"
        elif self.package_manager == "dnf":
            return f"dnf install -y {' '.join(packages)}"
        elif self.package_manager == "pacman":
            return f"pacman -S --noconfirm {' '.join(packages)}"

    def update_cmd(self):
        if self.package_manager == "apt":
            return "apt update && apt upgrade -y"
        elif self.package_manager == "dnf":
            return "dnf upgrade --refresh -y"
        elif self.package_manager == "pacman":
            return "pacman -Syu --noconfirm"
