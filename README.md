# Linux Tools Installer 🚀

A beautiful and intuitive CLI tool for installing and managing common Linux applications and services with a user-friendly interface.

## Features ✨

- 🎯 Simple interactive menu for installing applications
- 🔄 Automatic system package manager detection
- 📦 Support for multiple Linux distributions (Ubuntu, Debian, Fedora, CentOS, Arch, Alpine, Gentoo, OpenSUSE)
- 🛠️ Easy-to-use installer modules
- 📝 Detailed logging system
- 🎨 Beautiful terminal UI using Rich
- 🔍 Verbose mode for debugging

## Currently Supported Installers 📚

- 🐳 Docker + Portainer
- More coming soon...

## Requirements 📋

- Python 3.6 or higher
- Rich library
- Linux operating system
- Sudo access

## Installation 💻

1. Clone the repository:
```bash
git clone https://github.com/danpassol/pyinstaller.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 🔧

1. Run the installer:
```bash
sudo python3 menu.py
```

2. Select an installer from the menu
3. Follow the on-screen prompts
4. Enable verbose mode if needed for detailed output

## Adding New Installers 🛠️

Create a new Python file in the `installers` directory with a `run(verbose=False)` function:

```python
def run(verbose=False):
    # Your installation logic here
    pass
```

## Contributing 🤝

1. Fork the project
2. Create your installer branch (`git checkout -b feature/new-installer`)
3. Create your installer in the `installers` directory
4. Commit your changes (`git commit -m 'Add new installer'`)
5. Push to the branch (`git push origin feature/new-installer`)
6. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💪

If you encounter any issues or have questions, please:
- Open an issue in the repository
- Provide your distribution information
- Include any relevant error messages

---

Made with ❤️ by Your Name
