```ruby
╔═╝  ║    ╝  ╔═   ║ ║  ╔═╝  ║ ║
║    ║    ║  ║ ║  ╔╝   ╔═╝  ═╔╝
══╝  ══╝  ╝  ╝ ╝  ╝ ╝  ══╝   ╝
```
![GitHub License](https://img.shields.io/github/license/dim-gggl/Clinkey?style=plastic)
![PyPI - Version](https://img.shields.io/pypi/v/clinkey-cli?style=plastic&logo=python&logoColor=yellow)
![GitHub Release Date](https://img.shields.io/github/release-date/dim-gggl/clinkey-cli?style=plastic&logo=github&logoColor=green)


Your SECRET BUDDY for creating passwords you can actually remember.</div>Clinkey isn't your average password generator. It crafts strong, secure, and pronounceable passwords based on easy-to-remember syllables. Forget A9$fG!2p@k7z. Think TRENA-527-BROVO.🚀 InstallationThe easiest way is to use pipx (recommended for CLI tools) or pip.# With pipx (recommended)
pipx install clinkey-cli

# Or with pip
pip install clinkey-cli
For macOS users, you can also use Homebrew:# Replace <user>/<repo> with the actual tap path
brew install <user>/<repo>/clinkey-cli
✨ UsageClinkey works in two ways: Interactive Mode (cool and guided) or Direct Mode (fast and efficient).Interactive Mode 🎮Just run clinkey with no arguments to launch the slick, guided interface. It's the best way to get started!clinkey
Direct Commands ⚡Need a password, right now? Use flags to get what you want in a single line.# Create a 24-character "spicy" password (letters + digits)
clinkey -l 24 -t strong

# Generate 5 "inferno" passwords, all lowercase and without separators
clinkey -n 5 -t super_strong --lower --no-sep

# Save 10 "vanilla" passwords to a file
clinkey -n 10 -t normal -o my_passwords.txt
All the OptionsOptionAliasDescriptionAvailable Levels--length-lHow long do you want it?(a number)--type-tHow bold do you feel?normal (Vanilla 🍦)strong (Spicy 🔥)super_strong (Inferno 🌶️)--number-nHow many do you need?(a number)--no-sep-nsRemoves the - and _ separators.N/A--lower-lowFor a more discreet look (all lowercase).N/A--output-oSaves the loot to a file.(file path)📜 LicenseThis project is licensed under the MIT License. Use it wisely!