import argparse
from os import getcwd, path

from app.controllers.youtube_controller import (
    add_playlist_items_to_history_playlist, empty_playlist,
    get_authenticated_service)
from app.controllers.yt_dlp_controller import (download_playlist,
                                               parse_playlist_id)
from app.models.params import client_secrets_file, client_token_pickle
from app.utils.helpers import parse_urls_argument


def main():
    parser = argparse.ArgumentParser(description="YouTube Playlist Automation Tool")
    parser.add_argument("-l", "--urls", required=True, nargs='+',help="YouTube URL(s) containing the playlist ID. Give multiple URLs via: -l 'URL1' 'URL2' 'URL3'")
    parser.add_argument("-w", "--mark-watched", action="store_true", help="Mark items of playlist as watched")
    parser.add_argument("-d", "--delete-items", action="store_true", help="Delete items of playlist, but keep playlist")
    parser.add_argument("-D", "--download", action="store_true", help="Download all items of playlist")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start item of the playlist")
    parser.add_argument("-e", "--end", type=int, help="End item of the playlist")
    parser.add_argument("-f", "--formats", nargs='+',choices=['audio', 'video_720p', 'video_1080p', 'video_best'], 
                        default='video_720p', help="Download format choice")
    parser.add_argument("-o", "--output-path", default=getcwd(), help="Download path")

    args = parser.parse_args()
    url_list = parse_urls_argument(args.urls)

    len_diff = len(url_list)-len(args.formats)
    if len(url_list)>1 and len_diff>0:
        args.formats = args.formats + [args.formats[-1],]*len_diff

    for i,url in enumerate(url_list):
        # Authenticate and create YouTube API client
        playlist_id = parse_playlist_id(url)
        if not playlist_id:
            print("No playlist ID found in the URL.")
            continue
        print(f"Processing playlist: {url}")
        
        if not path.exists(client_secrets_file):
            raise FileNotFoundError(f"The client secrets file does not exist: {client_secrets_file}")

        if args.download:
            download_playlist(url, args.output_path, args.start, args.end, args.formats[i])
        
        if args.mark_watched or args.delete_items:
            try:
                youtube = get_authenticated_service(client_secrets_file,client_token_pickle)
            except Exception as e:
                print(f"Authentication failed: {e}")
                print("Please ensure your client_secret.json is valid and try again.")
                return
            
            if args.mark_watched:
                add_playlist_items_to_history_playlist(youtube, playlist_id)
            
            if args.delete_items:
                empty_playlist(youtube, playlist_id)
       
        print(f"Finished processing playlist: {url}\n") 

if __name__ == "__main__":
    main()


