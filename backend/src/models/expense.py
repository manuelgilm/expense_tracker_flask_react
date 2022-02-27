from src.db import db
from typing import List, Dict
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
