from flask import Flask, render_template, request, redirect, url_for, session

import sys
QRGENPATH = '../qr/'
sys.path.append(QRGENPATH)
import qrgen

import re

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/qrrequest', methods=['POST'])
def qrrequest():
    session['prefix'] = request.form['prefix']
    session['URL'] = request.form['URL']
    return redirect(url_for('qrcode'))

@app.route('/qrcode')
def qrcode():
    try:
        # Cookie test
        return render_template('qrcode.html', imgURL = qrURL(session['prefix'],session['URL']), URL = session['URL'], prefix = session['prefix'])
    except KeyError:
        return redirect(url_for('nocookies'))

@app.route('/nocookies')
def nocookies():
    return '<p>Looks like your cookies might not be enabled.</p><p>We hate cookies too, but you need them to use our site...</p><p>Enable your cookies for our domain and go <a href="/">back<a/></p>'

def qrURL(prefix,URL):
    '''Render QR code and return image URL.'''

    # TODO: Needs to be generalized to https
    URL = prefix+URL

    tempURL = './static/img/temp-'+re.sub('\W','_',URL)+'.png'

    img = qrgen.url2qr(URL,imgtype = 'png')
    img.save(tempURL)

    return tempURL

if __name__ == '__main__':
    app.run(debug=True)
