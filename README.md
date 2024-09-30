# autopYT -- a simple framework for YT-automation in python

The flow to make this magically work is:

1. User creates playlist with YT-movies of his/her liking
2. autopYT downloads them with a given formatting option
3. autopYT sets the playlist items as watched
4. autopYT deletes the items from the playlist to empty it for next movies

Connecting this with eg Syncthing allows to sync the results simply with any device thereby allowing to prepare everything on your laptop but watch the files on your mobile phone.


alias wlater='cd Projects/autopYT && conda activate autopYT && python main.py -D -l "test/urls.txt" -o "/sdcard/Movies/WlaterDL/"'