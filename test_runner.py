import argparse
from core.runner import CommandRunner

# Parse CLI args
parser = argparse.ArgumentParser(description="Test CommandRunner functionality.")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Pass verbose to the runner
runner = CommandRunner(verbose=args.verbose)

def test_install():
    print("\n[TEST] Installing btop and cava...")
    runner.install(["btop","cava"])

def test_upgrade():
    print("\n[TEST] Upgrading system...")
    runner.upgrade()

def test_remove():
    print("\n[TEST] Removing cava...")
    runner.remove(["cava"])

def test_run_command():
    print("\n[TEST] Running 'ls' command...")
    output = runner.run("ls", capture_output=True)
    if output is not None:
        print(output)

if __name__ == "__main__":
    test_install()
    test_upgrade()
    test_remove()
    test_run_command()

