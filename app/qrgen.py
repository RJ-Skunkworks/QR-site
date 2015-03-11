# qrgen.py

# Author: Roy Keyes (roy.coding@gmail)

import qrcode
import qrcode.image.svg
#import qrcode.image.svg.SvgFillImage

def url2qr(URL,filename = None, size = None, imgtype = 'svg'):
    '''Generate a QR code file for the given URL of specified size and type.

        Defaults to SVG format.'''

    if not filename:
        filename = URL2filename(URL)

    # Auto size if no size specified
    fit = False
    if not size:
        fit = True
    # TODO decide if we want to be able to specify size

    # Determine image format
    if imgtype == 'svg':
        qr = qrcode.QRCode(version=None, image_factory=qrcode.image.svg.SvgFillImage)
        suffix = '.svg'
    else:
        qr = qrcode.QRCode(version=None)
        suffix = '.png'

    if type(URL) == str or type(URL) == unicode:
        qr.add_data(URL)
        qr.make(fit=fit)
        img = qr.make_image()
        #img.save(filename+suffix)
    else:
        print 'URL parameter must be a string'
        raise TypeError

    return img

def parsefilename(filename):
    '''Parse file name and return sanitzied version.'''
    # Remove suffix and unwanted characters
    # TODO
    return filename

def URL2filename(URL):
    '''Create filename from URL.'''
    # TODO
    return True