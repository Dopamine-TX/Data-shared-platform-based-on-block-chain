from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid

# define profile.json constant, the file is used to
# save user name and password_hash
PROFILE_FILE = "profiles.json"

class User(UserMixin):
    def __init__(self, e_mail):
        self.id = e_mail

 
    @staticmethod
    def get(id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        return User(id)
       

