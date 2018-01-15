# pimaton

## Introduction

Pimaton is a simple photo booth application that can run on a raspberry pi with a PiCamera.

The principle is simple, it takes picture when triggered (configurable number), then generate a picture with all the taken pictures that can be printed (optional) or send somewhere (not developed yet)

The main goals of Pimaton are:
- To be simple (goal is to be installable via Pip soon)
- To be configurable ([check the config file](assets/default_config.yaml) to see all options, but number of images and their sizes can be changed. Even the background of the generated picture can be customized by using a template image based.
- To run either on CLI (still with camera preview thanks to PiCamera) or via a GUI (if X installed)
- To be triggered either via keyboard or via GPIO (if like me you want to plug an big arcade button :))
- If there is an internet connection:
  - To sync pictures on a web servers
  - And in GUI mode only:
    - To generate a QR code that link to a page to download taken picture taken and generated (the pic from the last loop, so people can just go download their pic they just tke instead of printing X times)
    - To ask for an email address to send the picture from the last loop (same as above)

I am sure i might have other ideas over time too :).


## The high level roadmap

- v0.0.1 (done):
  - Core architecture.
  - Take configurable pictures via picamera.
  - Generate an configurable image with the taken picture and an optional template.
- v0.0.2 (WIP):
  - Print picture via cups (done)
  - Manage PiCamera configuration
- v0.0.3:
  - Add optional GUI
- v0.0.4:
  - Add GPIO input option (might switch to v0.0.4)
  - Camera Flash capability
- v0.0.5:
  - Web features: Sync, email
- v0.0.6:
  - Translations
  - Additional GUI options: enable/disable flash
  - See slideshow of picture (either via button on GUI or as screensaver)
- v0.0.7:
  - Server + photo gallery web application (+ QR link compatible)
  - QR code link


# What can it do now ?

So far, the code in that repo can:
- Take pictures via the PiCamera (number and size configurable) (configuration of the PiCamera options to come soon)
- Generate an image based on the taken pictures (rendered image is configurable but be careful and test the rendering :p)
- Print the image via cups (so a printer needs to be installed)
- Only CLI mode for now
- Only Keyboard input for now


# TODO

- Implement a UI (but first choose the GUI lib…)
- Implement the GPIO input
- Implement all the web features.
- Add an option to use a simcard if no wifi is availble where you are.

Later on options to think about:

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

