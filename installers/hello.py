# installers/hello.py
def run(verbose=False):
    print("Hello installer running...")
    if verbose:
        print("Verbose mode is enabled.")
    else:
        print("Verbose mode is disabled.")
    # Simulate some installation steps  