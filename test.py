import os
import app
import unittest
import tempfile
from app.app_and_db import app, db
from app.startup.init_app import init_app
from app.posters.models import Item


class AppTestCase(unittest.TestCase):

    def setUp(self):
        _settings = dict(
            TESTING=True,               
            LOGIN_DISABLED=False,       
            MAIL_SUPPRESS_SEND=True,    
            SERVER_NAME='localhost',    
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:', 
            WTF_CSRF_ENABLED=False,    
            )

        init_app(app, db, _settings)
        app.app_context().push()
        self.app = app

    def tearDown(self):
        del self.app

    def test_database(self):
        db.create_all()
        item = Item(
            title='Masters', 
            allowed_posters=5, 
            price=00.99, 
            description='You get 5 posters, ability for custom urls, need 1 more feature.')
        
        db.session.add(item)
        db.session.commit()
        tester = Item.query.all() > 0
        self.assertTrue(tester)

if __name__ == '__main__':
    unittest.main()