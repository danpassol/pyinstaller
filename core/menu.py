# core/menu.py
# this version of the menu is more advanced than the simple_menu.py
# it uses the rich library to create a more user-friendly interface

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from core.logger import setup_logger
import os
import importlib

log = setup_logger()
console = Console()
INSTALLERS_DIR = "installers"

def list_installers():
    installers = []
    for file in os.listdir(INSTALLERS_DIR):
        if file.endswith(".py") and file != "__init__.py":
            installers.append(file[:-3])
    return installers

def show_menu():
    installers = list_installers()

    table = Table(title="🚀 Installer Menu", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", justify="center")
    table.add_column("Installer", style="green", justify="left")

    for idx, name in enumerate(installers, start=1):
        table.add_row(str(idx), f"Install {name.capitalize()}")

    exit_option = str(len(installers) + 1)
    table.add_row(exit_option, "Exit", style="bold red")

    console.print(table, justify="center")

    try:
        selection = int(Prompt.ask(f"\n[?] Select an option", default=exit_option))
    except ValueError:
        log.error("Invalid input. Please enter a number.")
        return None, False

    if selection == len(installers) + 1:
        log.info("Exiting installer.")
        return None, False

    if 1 <= selection <= len(installers):
        verbose = Confirm.ask("[?] Enable verbose mode?", default=False)
        return installers[selection - 1], verbose
    else:
        log.error("Invalid selection.")
        return None, False

def run_app():
    installer_name, verbose = show_menu()

    if installer_name:
        try:
            module = importlib.import_module(f"installers.{installer_name}")
            module.run(verbose=verbose)
        except ModuleNotFoundError:
            log.error(f"Module 'installers.{installer_name}' not found.")
        except AttributeError:
            log.error(f"Module 'installers.{installer_name}' does not have a 'run(verbose)' function.")
