# pimaton

## Introduction

Pimaton is a simple photo booth application that can run on a raspberry pi with a PiCamera.

The principle is simple, it takes picture when triggered (configurable number), then generate a picture with all the taken pictures that can be printed (optional) or send somewhere (not developed yet)

The main goals of Pimaton are:
- To be simple and instable quickly on a raspberrypi (goal is to be installable via Pip soon)
- To be configurable ([check the config file](assets/default_config.yaml) to see all options, but number of images and their sizes can be changed. Even the background of the generated picture can be customized by using a template image based.
- To run either on CLI (still with camera preview thanks to PiCamera) or via a GUI (if X installed, will run a TK app in fullscreen mode)
- To be triggered either via keyboard, touchscreen (if GUI + touchscreen) and/or via GPIO (if like me you want to plug an big arcade button :))
- If there is an internet connection:
  - To sync pictures on a web servers
  - And in GUI mode only:
    - To generate a QR code that link to a page to download taken picture taken and generated (the pic from the last loop, so people can just go download their pic they just tke instead of printing X times)
    - To ask for an email address to send the picture from the last loop (same as above)

I am sure i might have other ideas over time too :).


## The high level roadmap

- ~~v0.0.1 - core feature:~~
  - ~~Core architecture.~~
  - ~~Take configurable pictures via picamera.~~
  - ~~Generate an configurable image with the taken picture and an optional template.~~
- ~~v0.0.2 - print capabilities:~~
  - ~~Print picture via cups~~
  - ~~Manage PiCamera configuration~~
- v0.0.3 - GUI implementation (WIP, you can look at the [dedicated branch](https://git.bacardi55.org/bacardi55/pimaton/src/feature/%238-UI) to see it running (basic workflow works):
  - Add optional GUI
- v0.0.4 - Hardware:
  - Add GPIO input option (might switch to v0.0.4)
  - Camera Flash capability
- v0.0.5 - Web:
  - Sync
  - email
- v0.0.6 Main options:
  - Translations
  - Additional GUI options: enable/disable flash
  - See slideshow of picture (either via button on GUI or as screensaver)
- v0.0.7 Additional options:
  - Server + photo gallery web application (+ QR link compatible)
  - QR code link


# What can it do now ?

So far, the code in that repo can:
- Take pictures via the PiCamera (number, size, picamera option, … are configurable)
- Generate an image based on the taken pictures (rendered image is configurable but be careful and test the rendering :p)
- Can use a template image as the base for the rendered picture (to add text or decoration around the thumbnails)
- Print the image via cups (so a printer needs to be installed)
- Only CLI mode for now (but GUI work has started)
- Only Keyboard (TUI) or Touchscreen (GUI) input for now (GPIO and multiple input option coming soon)

# How to install ?

# Dependencies

Install python and pip. 
Install python-pil.imagetk if you want to use the GUI.

For now, clone the repository and go into the download directory, eg:

``` bash
git clone …
cd pimaton
```

Install the python extension (will be automated via pip)

```bash
pip install picamera six pyyaml pillow
# To be able to print
pip install pycups
```

Syntax to use Pimaton is:

```bash
usage: pimaton.py [-h] [--debug] [--config-file CONFIG_FILE] [-v]

Pimaton.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Show debug output
  --config-file CONFIG_FILE
                        Full path of the config file to load
  -v, --version         Display Pimaton version
```

Example:

```bash
python pimaton.py --config-dir=/path/to/config_file.yaml # Run pymathon with given config file - should be the "production mode" command.
python pimaton.py --debug # Display all debug messages and use default config file.
python pimaton.py --debug --config-file=/path/to/config_file.yml # Display all debug messages and use custom config file.
```

# TODO

- Implement a UI (work started on TK)
- Implement the GPIO input
- Look into the flash issue
- Implement all the web features.
- Add an option to use a simcard if no wifi is availble where you are.

Later on options to think about:

- System is already modular for main features (input, ui). Maybe I should work on a "modules" system to add the needed module not included in Pimaton code (eg: building a custom UI)
- Use CV2 to be able to work with additional camera

# Where can I find more info ? 

So far, only on [my blog](https://bacardi55.org/tags.html#pimaton) or in the code ^^".

You can contact me too via doing PR or mail if needed too.

# What is the hardware you are using?

- [A RaspberryPi 3B](https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-3-model-b)
- [A PiCamera](https://thepihut.com/collections/raspberry-pi-camera/products/raspberry-pi-camera-module?variant=758603005)
- [A 7" touchscreen display](https://thepihut.com/collections/raspberry-pi-screens/products/official-raspberry-pi-7-touchscreen-display?variant=4916536388) and its [case](https://thepihut.com/collections/raspberry-pi-screens/products/official-raspberry-pi-7-touchscreen-display?variant=4916536388)
- [A Canon Selphy CP1200](https://www.canon.fr/for_home/product_finder/printers/direct_photo/selphy_cp1200/) plugged in USB (*Nota* It doesn't work if you try to print via WiFi)
- [A Massive arcade button](https://www.adafruit.com/product/1185) (Very very big, you can't miss it even at 4am ^^)

