from core.distro import Distro

# Get the singleton instance once
distro = Distro()

def test_distro_detection():
    assert distro.id is not None, "Distro ID should be detected"
    assert distro.version_codename is not None, "Distro version should be detected"
    assert distro.package_manager is not None, "Package manager should be set"

    print(f"[TEST] Detected distribution: {distro.id} {distro.version_codename}")
    print(f"[TEST] Package manager: {distro.package_manager}")

def test_install_cmd():
    install_command = distro.install_cmd(["curl", "wget"])
    assert install_command is not None, "Install command should be generated"
    print(f"[TEST] Install command: {install_command}")

def test_update_cmd():
    update_command = distro.update_cmd()
    assert update_command is not None, "Update command should be generated"
    print(f"[TEST] Update command: {update_command}")

def test_remove_cmd():
    remove_command = distro.remove_cmd(["curl"])
    assert remove_command is not None, "Remove command should be generated"
    print(f"[TEST] Remove command: {remove_command}")

if __name__ == "__main__":
    test_distro_detection()
    test_install_cmd()
    test_update_cmd()
    test_remove_cmd()
    print("All tests passed!")
