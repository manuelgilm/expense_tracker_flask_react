from dbm import dumb
from pyexpat import model
from src.ma import ma 
from src.models.user import UserModel

class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
