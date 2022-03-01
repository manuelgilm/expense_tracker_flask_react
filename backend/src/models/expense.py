from src.db import db
from typing import List, Dict
from sqlalchemy import and_, func
import datetime 

class ExpenseModel(db.Model):
    __tablename__ =  'expenses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60))
    amount = db.Column(db.Float(precision=2),nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))


    @classmethod
    def find_expense_by_id(cls,_id:int)->"ExpenseModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_expenses_by_name(cls,name:str)->List:
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_expenses_by_owner(cls, user_id:int)->List:
        return cls.query.filter(cls.user_id == user_id)

    @classmethod
    def find_expense_by_id_and_owner(cls, expense_id:int, user_id:int)->"ExpenseModel":
        return cls.query.filter(and_(cls.user_id == user_id , cls.id == expense_id)).first()

    @classmethod
    def total_expenses_by_category(cls, user_id:int, category_id:int):
        return cls.query.with_entities(func.sum(cls.amount)).filter(and_(cls.user_id == user_id, cls.category_id == category_id)).first()

    @classmethod
    def total_expenses_by_user_id(cls, user_id:int):
        return cls.query.with_entities(func.sum(cls.amount)).filter(cls.user_id == user_id).first()

    @classmethod
    def find_expenses(cls)->List:
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
            "amount":self.amount,
            "date":self.date,
            "category_id":self.category_id,
            "user_id":self.user_id
        }
