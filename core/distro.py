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

                # use of dictionary to map the ID to a package manager instead of multiple if-elif statements
        package_managers = {
            "apt": ["ubuntu", "debian"],
            "dnf": ["rhel", "fedora", "centos"],
            "pacman": ["arch"],
            "apk": ["alpine"],
            "emerge": ["gentoo"],
            "zypper": [r"^opensuse"]  # regex pattern for anything starting with opensuse, this is because openSUSE has multiple versions like Tumbleweed, Leap, etc.
        }

        for manager, ids in package_managers.items():
            for distro_id in ids:
                if distro_id.startswith("^"):  # regex match
                    if re.match(distro_id, self.id):
                        self.package_manager = manager
                        return
                elif self.id == distro_id:
                    self.package_manager = manager
                    return

        raise Exception(f"Unsupported distro: {self.id}")

    def install_cmd(self, packages):
        return {
            "apt": f"apt install -y {' '.join(packages)}",
            "dnf": f"dnf install -y {' '.join(packages)}",
            "pacman": f"pacman -S --noconfirm {' '.join(packages)}",
            "apk": f"apk add {' '.join(packages)}",
            "emerge": f"emerge {' '.join(packages)}",
            "zypper": f"zypper install -y {' '.join(packages)}",
        }[self.package_manager]

    def update_cmd(self):
        return {
            "apt": "apt update && apt upgrade -y",
            "dnf": "dnf upgrade --refresh -y",
            "pacman": "pacman -Syu --noconfirm",
            "apk": "apk update && apk upgrade",
            "emerge": "emerge --sync && emerge --update --deep --newuse @world",
            "zypper": "zypper refresh && zypper update -y",
        }[self.package_manager]

    def remove_cmd(self, packages):
        return {
            "apt": f"apt purge -y {' '.join(packages)}",
            "dnf": f"dnf remove -y {' '.join(packages)}",
            "pacman": f"pacman -R --noconfirm {' '.join(packages)}",
            "apk": f"apk del {' '.join(packages)}",
            "emerge": f"emerge --unmerge {' '.join(packages)}",
            "zypper": f"zypper remove -y {' '.join(packages)}",
        }[self.package_manager]