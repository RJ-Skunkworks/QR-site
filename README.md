qrwebsite
=========
[![Build Status](https://travis-ci.org/RJ-Skunkworks/QR-site.svg?branch=master)](https://travis-ci.org/RJ-Skunkworks/QR-site)

##Development version of QR poster project

###Current requirements:

* [qr](https://github.com/RJ-Skunkworks/qr) from RJ-Skunkworks
* python-qrcode - via pip
* Flask - via pip
* Image - via pip (installs Pillow)
* Wand - via pip
* For converting PDF posters to png thumbnails
    * libmagickwand-dev for Linux
        * This installs via apt-get install on Debian/Ubuntu along with _a lot_ of dependencies
    * imagemagick for MacPorts/Homebrew on Mac

_See [requirements.txt](https://github.com/roycoding/qrwebsite/blob/master/requirements.txt)_

###Running the site
* You may need to change the variable _QRGENPATH_ in routing.py to be able to import the qr library.

```
python runserver.py
```
