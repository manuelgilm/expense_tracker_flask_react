from src.ma import ma 
from src.models.user import UserModel
from src.schemas.category import CategorySchema
from src.schemas.expense import ExpenseSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    categories = ma.Nested(CategorySchema, many=True, only=("name",))
    expenses = ma.Nested(ExpenseSchema, many = True, only=("name","amount"))

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True
        
        fields = ("username", "categories","expenses")
