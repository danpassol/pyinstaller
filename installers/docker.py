from core.runner import CommandRunner
from core.logger import setup_logger
import shutil

log = setup_logger()

def run(verbose=False):
    runner = CommandRunner(verbose=verbose)
    pm = runner.package_manager
    distro = runner.distro.id

    if shutil.which("docker"):
        log.error("Docker is already installed.")
        return
    
    log.info("Starting Docker installation...")
    
    log.warning("This script will install Docker, updating system packages and dependencies.")
    log.warning("Please ensure you have a backup of your system before proceeding.")
    
    choice = input("Press Enter to continue or type N to cancel... [Y/n] ").strip().lower()
    if choice in ["n", "N"]:
        log.error("Installation cancelled by user.")
        return
    
    runner.upgrade()

    install_steps = {
        "apt": [
            lambda: runner.install(["ca-certificates", "curl", "lsb-release", "gnupg",]),
            lambda: runner.run(
                "curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | "
                "gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg"),
            lambda: runner.run(
                "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] "
                "https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') "
                "$(lsb_release -cs) stable\" > /etc/apt/sources.list.d/docker.list"),
            lambda: runner.upgrade(),
            lambda: runner.install(["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]),
        ],
        "dnf": [
            lambda: runner.install(["dnf-plugins-core"]),
            lambda: runner.run(f"dnf config-manager --add-repo https://download.docker.com/linux/{distro}/docker-ce.repo"),
            lambda: runner.install(["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]),
        ],
        "pacman": [
            lambda: runner.install(["docker"]),
        ],
        "apk": [
            lambda: runner.install(["docker", "openrc"]),
        ],
        "zypper": [
            lambda: runner.install(["docker"]),
        ],
        "emerge": [
            lambda: runner.install(["app-containers/docker"]),
        ]
    }

    if pm not in install_steps:
        log.error(f"Docker installation not supported for package manager: {pm}")
        return

    for step in install_steps[pm]:
        step()

    start_cmds = [
        "systemctl start docker && systemctl enable docker",
        "service docker start",
        "rc-service docker start",
    ]
        
    for cmd in start_cmds:
        if runner.run(cmd, capture_output=False):
            log.info("Docker service started successfully.")
            break
    else:
        log.error("Failed to start Docker service. Please start it manually.")

    log.info("Docker installation completed successfully.")

    # Prompt for Portainer installation
    try:
        choice = input("Do you want to install Portainer? [Y/n]: ").strip().lower()
        if choice in ["", "y", "yes"]:
            install_portainer(runner)
        else:
            log.info("Skipping Portainer installation.")
    except KeyboardInterrupt:
        log.warning("Installation interrupted by user.")

def install_portainer(runner):
    log.info("Installing Portainer...")
    runner.run("docker volume create portainer_data")
    runner.run(
        "docker run -d -p 8000:8000 -p 9443:9443 --name portainer "
        "--restart=always -v /var/run/docker.sock:/var/run/docker.sock "
        "-v portainer_data:/data portainer/portainer-ce:latest"
    )
    log.info("Portainer installation completed and running at https://localhost:9443")

