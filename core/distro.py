# core/distro.py

import os
import re

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
                elif any(line.startswith(prefix) for prefix in ("VERSION_CODENAME=", "VERSION=")) and not self.version_codename:
                    self.version_codename = line.split("=")[1].strip().strip('"')

        if self.id in ["ubuntu", "debian"]:
            self.package_manager = "apt"
        elif self.id in ["rhel", "fedora", "centos"]:
            self.package_manager = "dnf"
        elif self.id in ["arch"]:
            self.package_manager = "pacman"
        elif self.id in ["alpine"]:
            self.package_manager = "apk"
        elif self.id in ["gentoo"]:
            self.package_manager = "emerge"
        elif re.match(r"^opensuse", self.id):
            self.package_manager = "zypper"
        else:
            raise Exception(f"Unsupported distro: {self.id}")

    def install_cmd(self, packages):
        if self.package_manager == "apt":
            return f"apt install -y {' '.join(packages)}"
        elif self.package_manager == "dnf":
            return f"dnf install -y {' '.join(packages)}"
        elif self.package_manager == "pacman":
            return f"pacman -S --noconfirm {' '.join(packages)}"
        elif self.package_manager == "apk":
            return f"apk add {' '.join(packages)}"
        elif self.package_manager == "emerge":
            return f"emerge {' '.join(packages)}"
        elif self.package_manager == "zypper":
            return f"zypper install -y {' '.join(packages)}"

    def update_cmd(self):
        if self.package_manager == "apt":
            return "apt update && apt upgrade -y"
        elif self.package_manager == "dnf":
            return "dnf upgrade --refresh -y"
        elif self.package_manager == "pacman":
            return "pacman -Syu --noconfirm"
        elif self.package_manager == "apk":
            return "apk update && apk upgrade"
        elif self.package_manager == "emerge":
            return "emerge --sync && emerge --update --deep --newuse @world"
        elif self.package_manager == "zypper":
            return "zypper refresh && zypper update -y"

    def remove_cmd(self, packages):
        if self.package_manager == "apt":
            return f"apt purge -y {' '.join(packages)}"
        elif self.package_manager == "dnf":
            return f"dnf remove -y {' '.join(packages)}"
        elif self.package_manager == "pacman":
            return f"pacman -R --noconfirm {' '.join(packages)}"
        elif self.package_manager == "apk":
            return f"apk del {' '.join(packages)}"
        elif self.package_manager == "emerge":
            return f"emerge --unmerge {' '.join(packages)}"
        elif self.package_manager == "zypper":
            return f"zypper remove -y {' '.join(packages)}"