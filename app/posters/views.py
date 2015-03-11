from flask_user import current_user, login_required
from app.app_and_db import app, db
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sys
import qrgen
import re
from app.pdf2png import pdfpreview
import os
from app.posters.forms import PosterCreateForm, BuyPosterForm
from app.posters.models import Poster, Item, Purchase
from app.users.models import User
import stripe

stripe.api_key = app.config['STRIPE_KEYS']['secret_key']

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
        
        current_user.remaining_posters -= 1
        
        db.session.add(current_user)
        
        db.session.add(entry)
        db.session.commit()

        
        # Redirect to home page
        return redirect(url_for('show_poster_page', slug= entry.slug))

    return render_template('posters/create_poster_page.html', form=form, remaining_posters= current_user.remaining_posters)

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


@app.route('/buy-posters')
def buy_posters_page():
    posters = Item.query.all()
    return render_template('posters/buy_posters_page.html', data=posters)
#     return """<http><body><form action="buy" method="POST">
# <script
#     src="https://checkout.stripe.com/checkout.js" class="stripe-button"
#     data-key="pk_test_w3qNBkDR8A4jkKejBmsMdH34"
#     data-amount="999"
#     data-name="jeffknupp.com"
#     data-description="Writing Idiomatic Python 3 PDF ($9.99)">
# </script>
# <input type="hidden" name="product_id" value="2" />
# </form>
# </body>
# </html>
# """

@app.route('/buy/<title>', methods=['GET'])
def buy(title=None):
    form = BuyPosterForm(request.form, product_id=title)
    prod  = Item.query.filter_by(title=title).first()

    return render_template('posters/purchase_poster.html', 
        key=app.config['STRIPE_KEYS']['publishable_key'], 
        product=prod)


@app.route('/charge', methods=['POST'])
def charge():
    
    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    prod  = Item.query.get(request.form['product_id'])

    try:
        charge = stripe.Charge.create(
                customer=customer.id,
                amount=int(prod.price*100),
                currency='usd',
                description="Posterlynx")

    except stripe.CardError, e:
        return """<html><body><h1>Card Declined</h1><p>Your chard could not
        be charged. Please check the number and/or contact your credit card
        company.</p></body></html>"""
    print charge

    purchase = Purchase(email=str(current_user.email),
                        product=prod.id)
    
    current_user.purchases.append(purchase)
    current_user.remaining_posters += prod.allowed_posters
    db.session.add(current_user)
    db.session.commit()

    return render_template('posters/poster_order_page.html', 
        data={ "paid": prod.price, "total": current_user.remaining_posters, "count": prod.allowed_posters} )
    # message = Message(
    #     subject='Thanks for your purchase!',
    #     sender="posterlynx", 
    #     html="""""",
    #     recipients=[email])
    # with mail.connect() as conn:
    #     conn.send(message)



def generate_qr(qr_data, obj):
    '''Render QR code and return image URL.'''
    
    file_name = obj.slug + "-" + obj.title + '.png'
    
    save_loc = os.path.join(app.config['QR_IMG_PATH'], file_name)

    img = qrgen.url2qr(qr_data, imgtype='png')
    img.save(save_loc)

    return "static/img/"+file_name