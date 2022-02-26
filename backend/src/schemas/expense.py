from src.ma import ma 
from src.models.expense import ExpenseModel

class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpenseModel
        load_instance = True
        include_fk = True
        fields = ("name","amount","category_id","user_id")