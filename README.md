# Twitch - Download All Highlights and Uploads

A Python package to download all highlights and uploads from a specified Twitch channel using twitch-dl. This tool was created in response to Twitch's announcement about implementing a 100-hour storage limit for highlights and uploads starting April 19, 2025, to help creators preserve their content before the limit takes effect.

Twitch will automatically delete highlights and uploads after April so no real need to delete them manually.

## Attribution

This tool is built on top of [twitch-dl](https://github.com/ihabunek/twitch-dl) by Ivan Habunek (ivan@habunek.com). The original twitch-dl is a fantastic CLI tool for downloading videos from Twitch.tv. This is simply a wrapper that adds automation for batch downloading all highlights and uploads from a channel.

All credit for the core downloading functionality goes to Ivan Habunek and the twitch-dl contributors.

## Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/thehamsti/twitch-dl-all.git
```

### Prerequisites

- Python 3.6 or higher (I recommend using [uv](https://docs.astral.sh/uv/) to manage your Python installations)
- [twitch-dl](https://twitch-dl.bezdomni.net/installation.html)
- [ffmpeg](https://ffmpeg.org/download.html)

### Quickstart

Install the packages:
```bash
pip install twitch-dl # If you haven't already installed twitch-dl
pip install git+https://github.com/thehamsti/twitch-dl-all.git

# Or with uv
uv pip install twitch-dl --system
uv pip install git+https://github.com/thehamsti/twitch-dl-all.git --system
```

**Note:** You'll need to re-source your shell after installing the packages.
```bash
source ~/.zshrc
# or
source ~/.bashrc
```

Run the script:
```bash
twitch-dl-all CHANNEL_NAME
```

### Running Without Installation

You can also run the script directly from the cloned repository:

1. Clone the repository:
```bash
git clone https://github.com/thehamsti/twitch-dl-all.git
cd twitch-dl-all
```

1. Run the script directly:
```bash
python -m twitch_dl_all.cli CHANNEL_NAME
```

## Usage

After installation, you can use the command-line tool:

```bash
twitch-dl-all CHANNEL_NAME
```

For example:
```bash
twitch-dl-all bananasaurus_rex
```

### Options

- `--downloads-dir DIR`: Specify the directory to save downloads (default: downloads)
- `--version`: Show program's version number and exit
- `-h, --help`: Show help message and exit

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [twitch-dl](https://github.com/ihabunek/twitch-dl) - The core downloading functionality (GPLv3 License)
- Ivan Habunek (ivan@habunek.com) - Creator of twitch-dl 