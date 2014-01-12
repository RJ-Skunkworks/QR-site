from flask import Flask, render_template, request, redirect, url_for, session

import sys
QRGENPATH = '../qr/'
sys.path.append(QRGENPATH)
import qrgen

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
    session['URL'] = request.form['URL']
    return redirect(url_for('qrcode'))

@app.route('/qrcode')
def qrcode():
    try:
        # Cookie test
        return render_template('qrcode.html', imgURL = qrURL(session['URL']), URL = session['URL'])
    except KeyError:
        return redirect(url_for('nocookies'))

@app.route('/nocookies')
def nocookies():
    return '<p>Looks like your cookies might not be enabled.</p><p>We hate cookies too, but you need them to use our site...</p><p>Enable your cookies for our domain and go <a href="/">back<a/></p>'

def qrURL(URL):
    '''Render QR code and return image URL.'''

    tempURL = './static/img/temp.png'

    print 'URL:',URL
    print 'type(URL):',type(URL)

    img = qrgen.url2qr(URL,imgtype = 'png')
    img.save(tempURL)

    return tempURL

if __name__ == '__main__':
    app.run(debug=True)
