# 📺 Control Chromecasts from Linux
Control your Chromecast via [MPRIS media player controls](https://specifications.freedesktop.org/mpris-spec/2.2/). 

MPRIS is the standard media player interface on Linux desktops.
`chromecast_mpris` allows you to control media playback on Chromecasts, and provides an interface for playback information.

MPRIS integration is [enabled by default](https://github.com/KDE/plasma-workspace/tree/master/applets/mediacontroller) in Plasma Desktop, and, along with GNOME's volume control widget, [there are widgets for GNOME](https://extensions.gnome.org/extension/1379/mpris-indicator-button/), too. [`playerctl` provides a CLI](https://github.com/altdesktop/playerctl) for controlling media players through MPRIS.

Check out [▶️mpris_server](https://github.com/alexdelorenzo/mpris_server) if you want to integrate MPRIS support into your media player.

## Screenshots

Controlling a Chromecast via Plasma Desktop's Media Player widget:

<img src="https://github.com/alexdelorenzo/chromecast_mpris/raw/master/assets/mpris.png" height="225" /> <img src="https://github.com/alexdelorenzo/chromecast_mpris/raw/master/assets/mpris_bar.png" height="225" />


## Features
  * [x] Control music and video playback
  * [x] Control app playback
  * [x] View playback information in real-time
  * [x] Display thumbnail and title
  * [x] Display playback position and media length
  * [x] Seek forward and backward
  * [x] Play, pause, and stop playback
  * [x] Volume up and down
  * [x] Play next and previous
  * [x] Quit current Chromecast app
  * [x] Open media from D-Bus
  * [x] Play YouTube videos
  * [ ] Playlist integration

## Installation
### Requirements
 - Linux / *BSD / [macOS](https://github.com/zbentley/dbus-osx-examples)
 - [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/)
 - Python >= 3.6
 - [PyGObject](https://pypi.org/project/PyGObject/)
 - `requirements.txt`
 
#### Installing PyGObject
On Debian-derived distributions like Ubuntu, install `python3-gi` with `apt`. 
On Arch, you'll want to install `python-gobject`, or install `chromecast_mpris` [directly from the AUR](https://aur.archlinux.org/packages/chromecast_mpris/).
On macOS, install [`pygobject3`](https://formulae.brew.sh/formula/pygobject3) via `brew`.

Use `pip` to install `PyGObject>=3.34.0` if there are no installation candidates available in your vendor's package repositories.

### PyPI
```bash
python3 -m pip install chromecast_mpris
```

You'll get a `chromecast_mpris` executable added to your `$PATH`.

### GitHub
Check out [the releases page on GitHub](https://github.com/alexdelorenzo/chromecast_mpris/releases) for stable releases.

If you'd like to use the development branch, clone the repository.

Once you have a source copy, run `python3 -m pip install -r requirements.txt`, followed by `python3 setup.py install`. 

You'll get a `chromecast_mpris` executable added to your `$PATH`.

### AUR

If you're on Arch, you can install `chromecast_mpris` [directly from the AUR](https://aur.archlinux.org/packages/chromecast_mpris/).

```bash
yay -S chromecast_mpris
```

### Upgrading

Stable releases are uploaded to PyPI. You can upgrade your `chromecast_mpris` installation like so:

```bash
python3 -m pip --upgrade chromecast_mpris
```

See the [releases page](https://github.com/alexdelorenzo/chromecast_mpris/releases) on GitHub.

## Usage
You'll need to make sure that your computer is on the same network as your Chromecasts, and that you're able to make connections to them. 

It also helps to know the names of the devices in advance.

### Help
```bash
$ chromecast_mpris --help
Usage: chromecast_mpris [OPTIONS]

  Control casting devices through MPRIS media controls.

Options:
  -n, --name TEXT         Specify a device name, otherwise control the first
                          device found.

  -h, --host TEXT         Hostname or IP address of streaming device.
  -u, --uuid TEXT         Streaming device's UUID.
  -w, --wait INTEGER      Retry after specified amount of seconds if a device
                          isn't found.

  -r, --retry-wait FLOAT  Seconds to wait between retries to reconnect after a
                          device connection is interrupted.  [default: 5.0]

  -l, --log-level TEXT    Debugging log level.  [default: WARN]
  --help                  Show this message and exit.
```

### Connecting to a Chromecast
Connect to a Chromecast named "My Chromecast" and run `chromecast_mpris` in the background.
```bash
$ chromecast_mpris -n "My Chromecast" &
[1] 1234
```

After launching `chromecast_mpris`, you can use any MPRIS client to interact with it. MPRIS support is built in directly to Plasma Desktop and GNOME 3, and you can use `playerctl` on the command-line. 

### Retrying until a Chromecast is found
You can use the `-w/--wait` flag to specify a waiting period in seconds before `chromecast_mpris` will try find a Chromecast again if one is not found initially.

For example, if you want to wait 60 seconds between scans for Chromecasts, you can run the following:
```bash
$ export SECONDS=60
$ chromecast_mpris -w $SECONDS
```

This is useful if you'd like to start `chromecast_mpris` at login, and there is a chance that your Chromecast isn't on, or you're on a different network. 

### Opening a URI on a Chromecast
 Get the D-Bus name for your Chromecast using `playerctl`.
```bash
$ playerctl -l
My_Chromecast
```

Use the D-Bus name to issue commands to it.

```bash
$ export URL="http://ccmixter.org/content/gmz/gmz_-_Parametaphoriquement.mp3"
$ playerctl -p My_Chromecast open "$URL"
```

This will play a song on the Chromecast.

## License
See `LICENSE`. Message me if you'd like to use this project with a different license.
