from src.ma import ma 
from src.models.category import CategoryModel
from src.schemas.expense import ExpenseSchema

class CategorySchema(ma.SQLAlchemyAutoSchema):
    expenses = ma.Nested(ExpenseSchema, many=True, only=("name","amount"))
    class Meta:
        model = CategoryModel
        load_instance = True
        load_only = ("user",)
        dump_only = ("id","name","description")
        include_fk = True

        fields = ("name","description","expenses")
