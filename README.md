# pimaton

## Introduction

Pimaton is a simple photo booth application that can run on a raspberry pi with a PiCamera.

The principle is simple, it takes picture when triggered (configurable number), then generate a picture with all the taken pictures that can be printed (optional) or send somewhere (optional)

[![pimaton_dryrun](https://git.bacardi55.org/bacardi55/pimaton/raw/master/docs/assets/pimaton_dryrun_thumbnail.jpg)](/docs/assets/pimaton_dryrun.jpg)

(The picture are not pixelized like this, I just "anonymized" them a bit^^)


If you want an idea of what it looks like when running, click on the image below (demo of v0.0.3, not v0.0.4 which is the last stable version at the moment):

[![QUICK DEMO](https://img.youtube.com/vi/HJ43O-nPQzw/0.jpg)](https://www.youtube.com/watch?v=HJ43O-nPQzw)

You can also find a gif of the GUI [here](https://bacardi55.org/2018/02/06/pimaton-is-now-installable-via-pip.html)

The booth is not mounted yet, but gives an idea of the application running and the speed to generate/print the image.

Goals were/are simple: easy installation, extensive configuration and options so it can be reused: 
- It's installable via "pip install pimaton".
- Two mode available: GUI (with python TK, you need X installed) or TUI. App can be triggered by touchscreen/mouse or keyboard. I'm planning to add a GPIO option too (to add a big hardware arcade button).
- Almost everything can be configured in a yaml file (from size of taken pictures, thumbnails, texts). Some features are optional, like actually printing the file or syncing them to a web server.
- The printed image can be customized via a template image to add things like texts (eg: "Wedding of Anakin Skywalker and Padmé Amidala") and/or adding decoration (eg: small light saber icon eveywhere). The app let you generate a blank template with the placeholder for the image to simplify the template creation.
- And a lot more done or planned :).

I am sure i might have other ideas over time too :).

**NOTA**:
- This is my first full python project (after some small contributions to other)
- This is my first pip package (i've tested it on my pi though :D)
- «It works on my rpi»
- I love merging pull request ;)


## What can it do now ?

So far, the code in that repo can:
- Take pictures via the PiCamera (number, size, picamera option, … are configurable)
- Generate an image based on the taken pictures (rendered image is configurable but be careful and test the rendering :p)
- Can use a template image as the base for the rendered picture (to add text or decoration around the thumbnails)
  - Can generate an empty template jpg file with placeholder to simplify base image creation. See [example](docs/assets/pimaton_template.jpg)
- Print the image via cups (so a printer needs to be installed)
- TUI (=CLI) or GUI mode available. Both are very simple though and nothing fancy yet.
- Multiple input to start taking pictures:
    - In TUI: Only Keyboard (Return key)
    - In GUI: Keyboard (Return key) **and/or** GUI button (can work with a mouse or directly via the Touchscreen if available)
    - (GPIO option for both TUI and GUI coming soon)
- Synchronise image via rsync on a remote server (you need to have rsync installed and an ssh-key without passphrase)
- Optional: Display a QR code on the GUI that link to a website (eg: a gallery of all the picitures).
- Optional: Print a QR code on the final picture to link to the direct page of the web gallery


## Installation

Install dependencies:

```bash
sudo apt install python-pip libjpeg-dev
pip install -U pip
# To enable GUI:
sudo apt install python-tk python-pil.imagetk
# To enable synchronizing image to a remote server
sudo apt install rsync
```

### Automated via Pip

(This is my first Pypi package, hope it works fine :D)

```bash
pip install pimaton
```

### Manual installation

Assuming here you have a working installation with python2.

Install the python extension (will be automated via pip later)

```bash
# Required libraries:
pip install picamera six pyyaml pillow
# To be able to print:
pip install pycups
```

Clone the repository and go into the download directory, eg:

``` bash
git clone https://git.bacardi55.org/bacardi55/pimaton.git
cd pimaton
# Run pimaton:
python pimaton.py # see Usage section for more example.
```

## Configuration

Copy one of the 2 configuration file.
```default_config.yaml``` contains the minimal config to work. It doesn't print the file, synchronise picture or manage QR code. Works only on GUI.
```default_config_full.yaml``` contains all option, and is configured by default to use the GUI and manage QR code. Sync and Print are disable but all options are shown as it requires configuration before enabling these feature.

```bash
cp /usr/local/lib/python2.7/dist-packages/pimaton/assets/default_config.yaml /path/to/myconfig.yaml
# OR
cp /usr/local/lib/python2.7/dist-packages/pimaton/assets/default_config_full.yaml /path/to/myconfig.yaml
```

Then edit it as you wish, but be careful with what you modify :). Hope the comments in the file are enough.

[See the dedicated page for the configuration](docs/configuration.md)

## Usage

```bash
usage: pimaton.py [-h] [--debug] [--single] [--config-file CONFIG_FILE]
                  [--generate-template] [-v]

Pimaton.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Show debug output
  --single              Only run 1 iteration
  --config-file CONFIG_FILE
                        Full path of the config file to load
  --generate-template   Generate a template image based on PiCamera
                        configuration
  -v, --version         Display Pimaton version
```

**Examples**:

To use Pimaton:

```bash
pimaton --config-file=/path/to/myconfig.yaml # Run pymathon with given config file - should be the "production mode" command.
pimaton --debug # Display all debug messages and use default minimal config file.
pimaton --debug --config-file=/path/to/myconfig.yaml # Display all debug messages and use custom config file.
```

If you want to run pimaton automatically once and quit, use the ```--single``` option. It will start pimaton, trigger the start automatically and quit after running once.

This can be useful for testing or if you want to script around pimaton (eg: integration with kalliope or other tools.)

```bash
pimaton --single # Run pimaton with default minimal configuration once.
pimaton --single --config-file=/path/to/myconfig.yaml # Run pimaton with custom configuration only once.
```

To generate a template file (empty based image with placeholder for thumbnails like [this example](docs/assets/pimaton_template.jpg):

```bash
# Generate template for default config:
pimaton --generate-template
# Generate template for custom config:
pimaton --config-file=/path/to/config_file.yaml --generate-template
# Generate template for custom config with debug output:
pimaton --debug --config-file=/path/to/config_file.yaml --generate-template
```


## The high level roadmap

The next planned item are:

- ~~[v0.0.1 - core feature](docs/roadmap.md):~~
- ~~[v0.0.2 - print capabilities](docs/roadmap.md):~~
- ~~[v0.0.3 - GUI implementation (WIP)](docs/roadmap.md):~~
- ~~[v0.0.4 - Web](docs/roadmap.md) ~~: Find a [full blog post](https://bacardi55.org/2018/02/13/having-all-pimaton-pictures-available-on-a-webgallery.html) and [an article about it](https://bacardi55.org/pimaton/part5-optional-webgallery.html)
- v0.0.5 - Hardware (To be started):
  - Add GPIO input option
  - Camera Flash capability

You can find the [full roadmap here](docs/roadmap.md)


## Where can I find more info ?

So far, only on [my blog](https://bacardi55.org/tags.html#pimaton) or in the code ^^" (but it still requires a lot of comments).

I've also created a [dedicated space on my site](https://bacardi55.org/pimaton.html)

You can find the todolist [here](docs/todo.md)

You can contact me too via doing PR or mail if needed too.

## What is the hardware you are using?

- [A RaspberryPi 3B](https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-b)
- [A PiCamera](https://thepihut.com/collections/raspberry-pi-camera/products/raspberry-pi-camera-module?variant=758603005)
- [A 7" touchscreen display](https://thepihut.com/collections/raspberry-pi-screens/products/official-raspberry-pi-7-touchscreen-display?variant=4916536388) and its [case](https://thepihut.com/collections/raspberry-pi-screens/products/official-raspberry-pi-7-touchscreen-display?variant=4916536388)
- [A Canon Selphy CP1200](https://www.canon.fr/for_home/product_finder/printers/direct_photo/selphy_cp1200/) plugged in USB (*Nota* It doesn't work if you try to print via WiFi)
- [A Massive arcade button](https://www.adafruit.com/product/1185) (Very very big, you can't miss it even at 4am ^^)

