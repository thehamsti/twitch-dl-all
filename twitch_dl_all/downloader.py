import json
import subprocess
import os
from datetime import datetime, timedelta
import time
import glob
from typing import List, Dict, Set, Optional


def run_twitch_dl_videos(channel: str, video_type: str) -> List[Dict]:
    """Fetch videos of a specific type from a channel."""
    try:
        cmd = ["twitch-dl", "videos", channel, "--json", "--all", "-t", video_type]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        videos = json.loads(result.stdout)
        videos = videos['videos']
        if not isinstance(videos, list):
            print(f"Error: Expected list of videos but got {type(videos)}")
            return []
        print(f"Found {len(videos)} {video_type} videos")
        return videos
    except subprocess.CalledProcessError as e:
        print(f"Error running twitch-dl: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        return []


def download_video(video_id: str, quality: str = "source") -> bool:
    """Download a single video."""
    # Check if the video is already being downloaded (partial file)
    existing_files = glob.glob(f"*_{video_id}_*")
    if existing_files:
        print(f"Found existing file(s) for video {video_id}:")
        for file in existing_files:
            print(f"- {file}")
        return True
        
    try:
        cmd = ["twitch-dl", "download", video_id, "-q", quality]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video {video_id}: {e}")
        print("Error output:")
        print(e.stderr)
        return False


def estimate_size(length_seconds: int) -> float:
    """Estimate file size in GB based on video length"""
    # Rough estimate assuming 8 Mbps bitrate for source quality
    bits = length_seconds * 8 * 1000000
    gb = bits / (8 * 1000 * 1000 * 1000)
    return round(gb, 2)


def format_duration(seconds: int) -> str:
    """Format seconds into human readable duration"""
    return str(timedelta(seconds=seconds))


def get_downloaded_videos() -> Set[str]:
    """Get list of already downloaded video IDs from filenames."""
    # twitch-dl creates files with pattern: [DATE] TITLE [ID].mp4 or .mkv
    files = glob.glob("*.mp4") + glob.glob("*.mkv") + glob.glob("*.part")
    video_ids = []
    print("\nScanning existing files:")
    for file in files:
        # Extract video ID from filename (last bracketed segment before extension)
        try:
            # Split by extension first to handle .part files
            base_name = file.rsplit('.', 1)[0]
            video_id = base_name.split("_")[1]
            video_ids.append(video_id)
        except IndexError:
            print(f"Could not extract video ID from filename: {file}")
            continue
    return set(video_ids)


def download_channel_videos(channel: str, downloads_dir: Optional[str] = "downloads") -> None:
    """Download all highlights and uploads from a channel."""
    # Create downloads directory if it doesn't exist
    if downloads_dir:
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        os.chdir(downloads_dir)

    # Get list of already downloaded videos
    downloaded_videos = get_downloaded_videos()
    print(f"Found {len(downloaded_videos)} already downloaded videos")

    # Get highlights and uploads
    print("Fetching highlights...")
    highlights = run_twitch_dl_videos(channel, "highlight")
    
    print("\nFetching uploads...")
    uploads = run_twitch_dl_videos(channel, "upload")

    # Combine and deduplicate videos
    all_videos = highlights + uploads
    unique_videos = {v["id"]: v for v in all_videos}.values()
    
    # Filter out already downloaded videos
    videos_to_download = [v for v in unique_videos if v["id"] not in downloaded_videos]
    
    if not videos_to_download:
        print("No new videos found to download!")
        return

    # Calculate total estimated size
    total_seconds = sum(v["lengthSeconds"] for v in videos_to_download)
    total_size = estimate_size(total_seconds)
    print(f"\nFound {len(videos_to_download)} new videos to download (estimated {total_size} GB total)")
    
    # Download each video
    total_videos = len(videos_to_download)
    completed = 0
    start_time = time.time()

    for video in videos_to_download:
        video_id = video["id"]
        title = video["title"]
        video_type = video["broadcastType"].lower()
        date = datetime.fromisoformat(video["recordedAt"].replace("Z", "+00:00")).strftime("%Y-%m-%d")
        duration = video["lengthSeconds"]
        size = estimate_size(duration)

        print(f"\nDownloading video {completed + 1}/{total_videos}")
        print(f"Title: {title}")
        print(f"Type: {video_type}")
        print(f"Date: {date}")
        print(f"Duration: {format_duration(duration)}")
        print(f"Estimated size: {size} GB")

        if completed > 0:
            elapsed_time = time.time() - start_time
            avg_time_per_second = elapsed_time / sum(v["lengthSeconds"] for v in list(videos_to_download)[:completed])
            remaining_seconds = sum(v["lengthSeconds"] for v in list(videos_to_download)[completed:])
            estimated_time = remaining_seconds * avg_time_per_second
            print(f"Estimated time remaining: {format_duration(int(estimated_time))}")

        success = download_video(video_id)
        if success:
            print("Download successful!")
            completed += 1
        else:
            print("Download failed!")

        # Add a small delay between downloads to prevent rate limiting
        time.sleep(1)

    print(f"\nDownloaded {completed}/{total_videos} new videos successfully!")
    print(f"Total videos in downloads folder: {len(downloaded_videos) + completed}") 