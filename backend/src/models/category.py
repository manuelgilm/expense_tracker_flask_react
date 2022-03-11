from src.db import db
from typing import List, Dict
from sqlalchemy import and_, func

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    expenses = db.relationship("ExpenseModel",lazy="dynamic")

    @classmethod
    def find_category_by_id(cls, _id:int)-> "CategoryModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_categories(cls)->List:
        return cls.query.all()

    @classmethod
    def find_categories_by_owner(cls, user_id:int)->List:
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def find_category_by_name_and_owner(cls, category_name:str, user_id:int)->"CategoryModel":
        return cls.query.filter(and_(cls.user_id==user_id, cls.name==category_name)).first()

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
