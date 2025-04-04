# SortMyShit

SortMyShit is an open-source Python project designed to help you organize and manage your files effortlessly. It provides customizable sorting rules to keep your directories clean and structured.

## Download

Latest version available for Linux [on SourceForge](https://sourceforge.net/projects/sortmyshit/)

## Features

- Automatically sort files based on extensions, names, or custom rules.
- Support for nested directories.
- Easy-to-use configuration file for custom sorting logic.
- Cross-platform compatibility.

## Installation

Clone the repository:

```bash
git clone https://github.com/noviplex/SortMyShit.git
cd SortMyShit
```

Create and use a virtual environment if needed (python3-venv required):

```bash
python3 -m venv .virtual
. .virtual/bin/activate 
```


Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the project:

```bash
python3 Main.py
```

Compile into a single executable (tested on Linux):

```bash
sh compile.sh
```

## VSCode support

Comes pre-configured to run in debugging mode with VSCode

Comes pre-configured with linting on vscode using flake8 

Comes pre-configured for testing using unittest with VSCode

## Licensing and Contrubition

See CONTRIBUTING.md and LICENSE files for more details

## Acknowledgments

Thanks to the open-source community for inspiration and support!
