# pdf2png.py

# Create preview PNG's of PDF posters

from wand.image import Image

def pdfpreview(filename, pngpath=None, width=400):
    '''Generate a PNG preview of a PDF document.'''

    if not pngpath:
        pngpath = filename+'.png'

    with Image(filename=filename) as img:
        img.format = 'png'
        scale = float(width)/img.width
        img.resize(int(scale*img.width),int(scale*img.height))
        img.save(filename=pngpath)

    return pngpath
