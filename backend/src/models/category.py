from src.db import db
from typing import List, Dict

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")
    

    def __init__(self, name:str, description:str, user_id:int)->None:
        self.name = name
        self.description = description
        self.user_id = user_id

    @classmethod
    def find_category_by_id(cls, _id:int)-> "CategoryModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_categories(cls)->List:
        return cls.query.all()

    def save_to_db(self)->None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)->None:
        db.session.delete(self)
        db.session.commit()

    def json(self)->Dict:
        return {
            "name":self.name,
            "description":self.description,
            "user_id":self.user_id,
        }
