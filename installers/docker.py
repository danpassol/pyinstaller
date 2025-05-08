from core.runner import CommandRunner
from core.logger import setup_logger
from core.progress import ProgressManager
import shutil

log = setup_logger()
progress_manager = ProgressManager()


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
            lambda: runner.install(["ca-certificates", "curl", "lsb-release", "gnupg"]),
            lambda: runner.run(
                "curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | "
                "gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg"
            ),
            lambda: runner.run(
                "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] "
                "https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') "
                "$(lsb_release -cs) stable\" > /etc/apt/sources.list.d/docker.list"
            ),
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

    try:
        # Initialize progress manager with 2 apps (Docker and optional Portainer)
        progress_manager.start(total_apps=2)

        # Docker installation
        app_steps_task_id = progress_manager.add_app("Docker", total_steps=len(install_steps[pm]))
        for step in install_steps[pm]:
            step_app_id = progress_manager.add_step("Docker", "Executing step...")
            step()
            progress_manager.complete_step(step_app_id)
            progress_manager.advance_app(app_steps_task_id)

        # Finalize Docker installation
        use_openrc = pm in ["apk", "emerge"]
        if use_openrc:
            runner.run("rc-service docker start")
        else:
            runner.run("systemctl start docker && systemctl enable docker")

        progress_manager.update_overall("[bold green]Docker installation complete!", advance=1)

        # Prompt for Portainer installation
        choice = input("Do you want to install Portainer? [Y/n]: ").strip().lower()
        if choice in ["", "y", "yes"]:
            install_portainer(runner)
        else:
            # Mark Portainer as skipped
            progress_manager.update_overall("[bold yellow]Portainer installation skipped.", advance=1)
            log.info("Skipping Portainer installation.")

    except Exception as e:
        log.error(f"An error occurred: {e}")
    finally:
        progress_manager.stop()


def install_portainer(runner):
    progress_manager.start(total_apps=1)
    log.info("Installing Portainer...")
    progress_manager.add_app("Portainer", total_steps=2)
    step_task_id = progress_manager.add_step("Portainer", "creating volume for data")
    runner.run("docker volume create portainer_data")
    progress_manager.complete_step(step_task_id)
    step_task_id = progress_manager.add_step("Portainer", "creating volume for data")
    runner.run(
        "docker run -d -p 8000:8000 -p 9443:9443 --name portainer "
        "--restart=always -v /var/run/docker.sock:/var/run/docker.sock "
        "-v portainer_data:/data portainer/portainer-ce:latest"
    )
    progress_manager.complete_step(step_task_id)
    progress_manager.update_overall("[bold green]Porainer installation complete!", advance=1)
    progress_manager.stop()

    log.info("Portainer installation completed and running at https://localhost:9443")

