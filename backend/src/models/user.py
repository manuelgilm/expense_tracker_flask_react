from src.db import db
from typing import List

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)

    categories = db.relationship('CategoryModel', lazy="dynamic", backref = "user_categories")
    expenses = db.relationship('ExpenseModel', lazy = "dynamic", backref = "user_expenses")

    @classmethod
    def find_by_username(cls, username:str)->"UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_users(cls)->List:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id:int)->"UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self)->None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)->None:
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "username":self.username,
            "password":self.password
        }


