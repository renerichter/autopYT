b# Android Setup

## Goals

## Steps

### MAC prepare

* install adb and scrcpy via `brew install adb scrcpy`

### Android Prepare

* connect Android-phone via USB to MAC and allow access
* unlock USB-debugging
    * Go to Settings > About phone.
    * Tap Build number seven times to enable Developer Options.
    * Go to Settings > System > Developer options and enable USB debugging.
* in cli run `scrcpy` and connect to android-phone to control via mac
* install termux + grant complete access rights (termux-setup-storage) to be able to access files eg from sdcard
* in termux
    * create folder Transfer on sdcard `mkdir /sdcard/Transfer/` for simple and organized file-transfer between MAC and Android
        * NOTE: non-rooted devices (as used for this example) do not grant external admin or file-access via `adb` except for `/sdcard` path
    * install `proot-distro`
        * `pkg install proot-distro`
        * `proot-distro install ubuntu`
        * `proot-distro login ubuntu`
        * `apt update && apt upgrade`
        * `apt install ffmpeg` as needed later for file conversion
* create new user `useradd -m -s /bin/bash myUser` with home-directory (avoid pwd for now)
* exit `proot-distro`
* create alias for simple login via `nano .bashrc`
    * `alias logMeIn='proot-distro login ubuntu --user myUser`
* `source .bashrc`
* `logMeIn`
    * create `Projects`-folder via `mkdir Projects`
    * install miniforge for linux64
        * `wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh && bash Miniforge3-Linux-aarch64.sh`

### Copy Option 1: using ADB

Benefit of this method: Directly able to copy environment settings, secrets and test-files.</br>
Assumes devices (android and mac) are still connected.

* on MAC in cli
    * `adb push "/path/on/mac/to/autopYT" "/sdcard/Transfer/"`
* on Android (via `scrcpy`)
    * within `proot-distro` as `myUser` copy to Projects-folder via `cd Projects/ && cp -r /sdcard/Transfer/autopYT . && cd autopYT`
    * install new mamba environment `mamba env create -f environment_noVer.yml`
    * activate `mamba activate autopYT` and test `python main.py -h`
    * then run: `python main.py -D -l "test/urls.txt" -o "/sdcard/Movies/WlaterDL"`

### Copy Option 2: Github

* follow soon

### Convenience

* create alias for ease within `myUser` on `proot-distro`
    * `alias getAndDelete='mamba activate autopYT && cd /home/myUser/Projects/autopYT && python main.py -Dd -l "test/urls.txt" -o "/sdcard/Movies/WlaterDL"'`
* create function for alias-call directly within termux main-level -> **not working as intended**
    * `getThem(){ logMeIn; getAndDelete; }` (be cautious with the spacings!)

## Status

* tested for [MacBook Pro M1](https://support.apple.com/en-us/111902) and [Google Pixel 7](https://en.wikipedia.org/wiki/Pixel_7)
