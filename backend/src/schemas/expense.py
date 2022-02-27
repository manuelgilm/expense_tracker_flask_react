from src.ma import ma 
from src.models.expense import ExpenseModel

class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpenseModel
        load_instance = True
        include_fk = True
        dump_only = ("id",)
        fields = ("name","description","amount","user_id","category_id")