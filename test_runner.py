# test_runner.py

from core.runner import CommandRunner

def test_install():
    print("\n[TEST] Installing curl...")
    runner = CommandRunner()
    runner.install(["curl"])

def test_upgrade():
    print("\n[TEST] Upgrading system...")
    runner = CommandRunner()
    runner.upgrade()

def test_remove():
    print("\n[TEST] Removing curl...")
    runner = CommandRunner()
    runner.remove(["curl"])

def test_run_command():
    print("\n[TEST] Running 'ls' command...")
    runner = CommandRunner()
    output = runner.run("ls", capture_output=True)
    print("[OUTPUT]")
    print(output)

if __name__ == "__main__":
    test_install()
    test_upgrade()
    test_remove()
    test_run_command()
