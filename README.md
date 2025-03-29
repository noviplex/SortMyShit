# SortMyShit

SortMyShit is an open-source Python project designed to help you organize and manage your files effortlessly. It provides customizable sorting rules to keep your directories clean and structured.

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

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b [feature/fix]/[feature-name]`.
3. Commit your changes following the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) syntax: `git commit -m "type(scope): description"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project and all of its code is licensed under the [MIT License](https://mit-license.org/).

## Acknowledgments

Thanks to the open-source community for inspiration and support!
