from functools import partial
from os import makedirs, path
from re import findall
from urllib.parse import parse_qs, urlparse

import yt_dlp


def get_playlist_name(url):
    playlist_options = {
        'extract_flat': True,  # This option helps to fetch playlist info without detailed extraction
        'playlistend': 1,       # Only extract the first video in the playlist for initial testing
        'quiet': True,}
    with yt_dlp.YoutubeDL(playlist_options) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'Unnamed_Playlist')

def to_camel_case(text):
    words = findall(r'\w+', text)
    return ''.join(word.capitalize() for word in words)

def parse_playlist_id(url:str):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('list', [None])[0]

def grab_process_error(info_dict,failed_urls):
    """Hook function to process errors and store failed URLs."""
    # Check if the info_dict has an error message
    if 'error' in info_dict:
        failed_urls.append(info_dict['url'])
    return None

def download_playlist(url, download_path, start=1, end=None, format_choice='video_720p'):
    failed_urls = []
    partial_grab_process_error = partial(grab_process_error,failed_urls=failed_urls)
    

    playlist_name = get_playlist_name(url)
    folder_name = to_camel_case(playlist_name)
    folder_path = path.join(download_path, folder_name)
    makedirs(folder_path, exist_ok=True)

    format_options = {
        'audio': 'bestaudio/best',
        'video_720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'video_1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'video_best': 'bestvideo+bestaudio/best'
    }

    ydl_opts = {
        'format': format_options.get(format_choice, 'bestvideo+bestaudio/best'),#format_options[format_choice],
        'outtmpl': f'{folder_path}/%(playlist_index)s-%(title)s.%(ext)s',
        'playliststart': start,
        'playlistend': end,
        'progress_hooks':[partial_grab_process_error],  # Hook to process errors
        'noplaylist': False,  # Ensure playlist is processed
    }

    if format_choice != 'audio':
        ydl_opts.update({
            'embedmetadata': True,
            'embedchapters': True,
            'writesubtitles': False,
            'subtitleslangs': ['en','de'],
            'embedsubs': True,
            'merge_output_format': 'mp4',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"An error occurred while downloading {url}: {e}")
            # print("Trying with best available format...")
            # ydl_opts['format'] = 'best'
            # with yt_dlp.YoutubeDL(ydl_opts) as ydl_fallback:
            #     try:
            #         ydl_fallback.download([url])
            #     except Exception as e:
            #         print(f"Failed to download even with best format: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while downloading {url}: {e}")

    # Print or process failed URLs
    print("Failed URLs:", failed_urls)
