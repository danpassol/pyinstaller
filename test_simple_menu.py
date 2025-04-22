from core.simple_menu import show_menu
import importlib

if __name__ == "__main__":
    installer_name, verbose = show_menu()
    
    # this part would be on install.py, this is just for testing purposes, 
    # the menu only responses with the name of the installer and the verbose option

    if installer_name:
        try:
            module = importlib.import_module(f"installers.{installer_name}")
            module.run(verbose=verbose)
        except ModuleNotFoundError:
            print(f"[ERROR] Could not find module 'installers.{installer_name}'")
        except AttributeError:
            print(f"[ERROR] Module 'installers.{installer_name}' has no 'run()' function")
