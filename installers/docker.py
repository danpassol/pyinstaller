from core.runner import CommandRunner
from core.logger import setup_logger
from core.distro import Distro

def run(verbose=False):

    log = setup_logger()
    distro = Distro()
    runner = CommandRunner(verbose=verbose)

    if verbose:
        log.info("Verbose mode enabled.")
    try:
        runner.run("docker --version")
        log.info("Docker is already installed.")
        return
    except Exception as e:
        log.error(f"Error checking Docker installation: {e}")

    log.info("Installing dependencies...")
    runner.install(["curl", "ca-certificates", "gnupg", "lsb-release"])
    