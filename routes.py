from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

import sys
QRGENPATH = '../qr/'
sys.path.append(QRGENPATH)
import qrgen

import re

import pdf2png

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Get user input to generate a QR code
@app.route('/qrrequest', methods=['POST'])
def qrrequest():
    session['qr.prefix'] = request.form['prefix']
    session['qr.URL'] = request.form['URL']
    return redirect(url_for('qrcode'))

# Get user input to generate a poster page and QR code
@app.route('/pagegen', methods=['POST'])
def pagegen():
    session['poster.posterfile'] = request.form['posterfile']
    session['poster.title'] = request.form['title']
    session['poster.authors'] = request.form['authors']
    session['poster.contact'] = request.form['contact']
    session['poster.conf'] = request.form['conf']
    session['poster.date'] = request.form['date']
    session['poster.abstract'] = request.form['abstract']
    return redirect(url_for('posterpage'))

def cookiecheck(f):
    '''Check if cookies are on.'''
    @wraps(f)
    def cookiewrap():
        if session:
            return f()
        else:
            return redirect(url_for('nocookies'))
    return cookiewrap

@app.route('/qrcode')
@cookiecheck
def qrcode():
    return render_template('qrcode.html', imgURL = qrURL(session['qr.prefix'],session['qr.URL']), URL = session['qr.URL'], prefix = session['qr.prefix'])

@app.route('/posterpage')
@cookiecheck
def posterpage():
    # For dev at this point just use a single page / URL
    prefix = 'http://'
    URL = '127.0.0.1:5000' + url_for('posterpage')
    return render_template('posterpage.html', data = session, imgURL = qrURL(prefix,URL), URL=URL, prefix=prefix, pngpath=pdf2png.pdfpreview(session['poster.posterfile'], './static/img/'+session['poster.posterfile'].split('/')[-1]+'.png'))

@app.route('/nocookies')
def nocookies():
    return '<p>Looks like your cookies might not be enabled.</p><p>We hate cookies too, but you need them to use our site...</p><p>Enable your cookies for our domain and go <a href="/">back<a/></p>'

def qrURL(URL,prefix='http'):
    '''Render QR code and return image URL.'''
    URL = prefix+URL

    tempURL = './static/img/temp-'+re.sub('\W','_',URL)+'.png'

    img = qrgen.url2qr(URL,imgtype = 'png')
    img.save(tempURL)

    return tempURL

if __name__ == '__main__':
    app.run(debug=True)
