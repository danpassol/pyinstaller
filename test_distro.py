# test_distro.py

from core.distro import Distro

def test_distro_detection():
    distro = Distro()
    
    assert distro.id is not None, "Distro ID should be detected"
    assert distro.version is not None, "Distro version should be detected"
    assert distro.package_manager is not None, "Package manager should be set"

    print(f"Detected distribution: {distro.id} {distro.version}")
    print(f"Package manager: {distro.package_manager}")

def test_install_cmd():
    distro = Distro()
    install_command = distro.install_cmd(["curl", "wget"])
    
    assert install_command is not None, "Install command should be generated"
    print(f"Install command: {install_command}")

def test_update_cmd():
    distro = Distro()
    update_command = distro.update_cmd()
    
    assert update_command is not None, "Update command should be generated"
    print(f"Update command: {update_command}")

if __name__ == "__main__":
    test_distro_detection()
    test_install_cmd()
    test_update_cmd()
    print("All tests passed!")
