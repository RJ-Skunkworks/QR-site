from flask_user import current_user, login_required
from app.app_and_db import app, db
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sys
import qrgen
import re
from app.pdf2png import pdfpreview
import os
from app.posters.forms import PosterCreateForm
from app.posters.models import Poster

# Get user input to generate a QR code
@app.route('/qrrequest', methods=['POST'])
def qrrequest():
    session['qr.prefix'] = request.form['prefix']
    session['qr.URL'] = request.form['URL']
    return redirect(url_for('qrcode'))

# Get user input to generate a poster page and QR code

@app.route('/create', methods=['POST','GET'])
@login_required
def create_poster_page():
    form = PosterCreateForm(request.form)
    
    if request.method=='POST' and form.validate():
        
        entry = Poster()
        entry.user_id = current_user.id
        form.populate_obj(entry)

        entry.qr_image = generate_qr(request.headers['Host']+"/"+entry.slug, entry)
        db.session.add(entry)
        db.session.commit()
        
        # Redirect to home page
        return redirect(url_for('show_poster_page', slug= entry.slug))

    return render_template('posters/create_poster_page.html', form=form)

@app.route('/list', methods=['GET'])
@login_required
def list_poster_page():

    posters = Poster.query.filter_by(user_id=current_user.id).all()
    # print(posters)
    return render_template('posters/list_poster_page.html', data=posters)


@app.route('/qrcode')
def qrcode():
    return render_template('pages/qrcode_page.html', imgURL = qrURL(session['qr.prefix'],\
    session['qr.URL']), URL = session['qr.URL'], prefix = session['qr.prefix'])

@app.route('/<slug>')
def show_poster_page(slug=None):
    # For dev at this point just use a single page / URL
    
    poster = Poster.query.filter_by(slug=slug).first()
    return render_template('posters/show_poster_page.html', data=poster)

def generate_qr(qr_data, obj):
    '''Render QR code and return image URL.'''
    
    file_name = obj.slug + "-" + obj.title + '.png'
    
    save_loc = os.path.join(app.config['QR_IMG_PATH'], file_name)

    img = qrgen.url2qr(qr_data, imgtype='png')
    img.save(save_loc)

    return "static/img/"+file_name