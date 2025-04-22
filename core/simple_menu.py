# core/simple_menu.py
# BEWARE: This file is not part of the final version of the code. 
# It is a simple menu to test the functionality of the installer system.

import os
from core.logger import setup_logger

log = setup_logger()

INSTALLERS_DIR = "installers"

def list_installers():
    installers = []
    for file in os.listdir(INSTALLERS_DIR):
        if file.endswith(".py") and file != "__init__.py":
            installers.append(file[:-3])  # Remove .py extension
    return installers

def show_menu():
    print("\n===== Installer Menu =====")
    installers = list_installers()

    for idx, name in enumerate(installers, start=1):
        print(f"{idx}) Install {name}")

    print(f"{len(installers) + 1}) Exit")

    try:
        selection = int(input("\n[?] Select an option [1-{}]: ".format(len(installers) + 1)))
    except ValueError:
        log.error("Invalid input. Please enter a number.")
        return None, False

    if selection == len(installers) + 1:
        log.info("Exiting installer.")
        return None, False

    if 1 <= selection <= len(installers):
        verbose = input("[?] Enable verbose mode? [y/N]: ").strip().lower() == 'y'
        return installers[selection - 1], verbose
    else:
        log.error("Invalid selection.")
        return None, False
