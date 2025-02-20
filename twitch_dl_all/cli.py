import argparse
import sys
from . import __version__
from .downloader import download_channel_videos


def main():
    parser = argparse.ArgumentParser(
        description="Download all highlights and uploads from a Twitch channel"
    )
    parser.add_argument(
        "channel",
        help="Twitch channel name"
    )
    parser.add_argument(
        "--downloads-dir",
        default="downloads",
        help="Directory to save downloads (default: downloads)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    try:
        download_channel_videos(args.channel, args.downloads_dir)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 