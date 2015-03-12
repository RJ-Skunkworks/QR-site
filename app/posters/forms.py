from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, DateField, HiddenField, validators



class PosterCreateForm(Form):
	       
    title = StringField('Poster title', validators=[
        validators.DataRequired('Title is required')])
    date = StringField("Event date", validators=[
        validators.DataRequired('Please use 02-4-2015 format.')])
    # authors = StringField('Authors', validators=[
    #     validators.DataRequired('Authors are required')])
    slug = StringField('Custom-URL')
    abstract = TextAreaField('Abstract')
    contact = StringField('Contact (public)')
    submit = SubmitField('Save')

# Define the User profile form
class BuyPosterForm(Form):
    # product_id = HiddenField()
    # product_id = HiddenField()
    submit = SubmitField('Buy')