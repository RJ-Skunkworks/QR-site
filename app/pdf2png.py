# pdf2png.py

# Create preview PNG's of PDF posters

from wand.image import Image
import subprocess, shlex

def pdfpreview(filename, pngpath=None, width=400, subproc=True):
    '''Generate a PNG preview of a PDF document.'''

    if not pngpath:
        pngpath = filename+'.png'

    # By default run ImageMagick directly instead of Wand
    if subproc:
        command = "convert " + filename + " -resize " + str(width) + "x1000\> " + pngpath
        subprocess.Popen(shlex.split(command))
    else:
        with Image(filename=filename) as img:
            img.format = 'png'
            scale = float(width)/img.width
            img.resize(int(scale*img.width),int(scale*img.height))
            img.save(filename=pngpath)

    return pngpath

#if __name__ == '__main__':
#    import timeit
#    testpdf = '/home/roy/Dropbox/Medical_Physics/AAPM-2010/Cloud/poster/AAPM-2010-cloud-poster.pdf'
#    testpng = 'test-convert.png'
#    print timeit.timeit("pdfpreview('/home/roy/Dropbox/Medical_Physics/AAPM-2010/Cloud/poster/AAPM-2010-cloud-poster.pdf', 'test-convert.png',subproc=False)",number=3, setup="from __main__ import pdfpreview")
