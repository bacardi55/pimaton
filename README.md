# pimaton

## Introduction

Pimaton is a simple photo booth application that can run on a raspberry pi with a PiCamera.

The principle is simple, it takes picture when triggered (configurable number), then generate a picture with all the taken pictures that can be printed (optional) or send somewhere (not developed yet)

[![pimaton_dryrun](https://git.bacardi55.org/bacardi55/pimaton/raw/master/docs/assets/pimaton_dryrun_thumbnail.jpg)](/docs/assets/pimaton_dryrun.jpg)

(The picture are not pixelized like this, I just "anonymized" them a bit^^)

The main goals of Pimaton are:
- To be simple and instable quickly on a raspberrypi (goal is to be installable via Pip soon)
- To be configurable ([check the config file](assets/default_config.yaml) to see all options
  - Options include (but not limited to), number of picture taken, size of thumbnails and their layout on printed image. A background/template image can be used to customize the final image.
  - A command is included to generate a blank template with placeholder for the future image to facilitate template creation. See [example](docs/assets/pimaton_template.jpg)
- To run either on CLI (still with camera preview thanks to PiCamera) or via a GUI (if X installed, will run a TK app in fullscreen mode)
- To be triggered either via keyboard, touchscreen (if GUI + touchscreen) and/or via GPIO (if like me you want to plug an big arcade button :))
- If there is an internet connection:
  - To sync pictures on a web servers
  - And in GUI mode only:
      - To generate a QR code that link to a page to download taken picture taken and generated (the pic from the last loop, so people can just go download their pic they just tke instead of printing X times)
      - To ask for an email address to send the picture from the last loop (same as above)

I am sure i might have other ideas over time too :).


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

## Installation

Install dependencies:

```bash
sudo apt install python-pip libjpeg-dev
pip install -U pip
# To enable GUI:
sudo apt install python-tk python-pil.imagetk
```

### Automated via Pip

```bash
pip install pimaton
```

### Manual installation

Assuming here you have a working installation with python2 and pip.

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

[See the dedicated page for the configuration](docs/configuration.md)

## Usage

```bash
usage: pimaton.py [-h] [--debug] [--config-file CONFIG_FILE]
                  [--generate-template] [-v]

Pimaton.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Show debug output
  --config-file CONFIG_FILE
                        Full path of the config file to load
  --generate-template   Generate a template image based on PiCamera
                        configuration
  -v, --version         Display Pimaton version
```

**Examples**:

To use Pimaton:

```bash
python pimaton.py --config-dir=/path/to/config_file.yaml # Run pymathon with given config file - should be the "production mode" command.
python pimaton.py --debug # Display all debug messages and use default config file.
python pimaton.py --debug --config-file=/path/to/config_file.yml # Display all debug messages and use custom config file.
```

To generate a template file (empty based image with placeholder for thumbnails like [this example](docs/assets/pimaton_template.jpg):

```bash
# Generate template for default config:
python pimaton.py --generate-template
# Generate template for custom config:
python pimaton.py --config-file=/path/to/config_file.yaml --generate-template
# Generate template for custom config with debug output:
python pimaton.py --debug --config-file=/path/to/config_file.yaml --generate-template
```


## The high level roadmap

The next planned item are:

- ~~v0.0.1 - core feature:~~
- ~~v0.0.2 - print capabilities:~~
- v0.0.3 - GUI implementation (WIP):
  - ~~Add optional GUI~~:
      - ~~Implement basic UI with all screens (waiting, processing and thankyou screen)~~
      - ~~Touchscreen input to start process~~
      - ~~Make it pretty (stuff I don't like/know how to do :P)~~
      - ~~Put a picture (either 1st taken pic or an animated gif) on the processing screen~~
      - ~~Make all text configurable~~
      - ~~Implement a "statistics" area in the header (eg: "X pic has been taken since Pimaton starter")~~
  - ~~Add PiCamera overlay (countdown between pictures)~~
  - ~~Implement multi input in in both TUI and GUI mode~~ (for now: 'keyboard' and/or 'gui' - only 'keyboard' is usable in TUI mode so far)
  - ~~Add a command to generate the template file to facilitate user to personalize it~~
  - Create pip package (will be usable (in a rough state) when tagging v0.0.3)
- v0.0.4 - Hardware (Might become v0.0.5):
  - Add GPIO input option
  - Camera Flash capability
- v0.0.5 - Web (might become v0.0.4):
  - Sync
  - email

You can find the [full roadmap here](docs/roadmap.md)


## Where can I find more info ?

So far, only on [my blog](https://bacardi55.org/tags.html#pimaton) or in the code ^^" (but it still requires a lot of comments).

You can find the todolist [here](docs/todo.md)

You can contact me too via doing PR or mail if needed too.

## What is the hardware you are using?

- [A RaspberryPi 3B](https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-b)
- [A PiCamera](https://thepihut.com/collections/raspberry-pi-camera/products/raspberry-pi-camera-module?variant=758603005)
- [A 7" touchscreen display](https://thepihut.com/collections/raspberry-pi-screens/products/official-raspberry-pi-7-touchscreen-display?variant=4916536388) and its [case](https://thepihut.com/collections/raspberry-pi-screens/products/official-raspberry-pi-7-touchscreen-display?variant=4916536388)
- [A Canon Selphy CP1200](https://www.canon.fr/for_home/product_finder/printers/direct_photo/selphy_cp1200/) plugged in USB (*Nota* It doesn't work if you try to print via WiFi)
- [A Massive arcade button](https://www.adafruit.com/product/1185) (Very very big, you can't miss it even at 4am ^^)

