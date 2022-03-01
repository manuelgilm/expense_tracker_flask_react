from src.ma import ma 
from src.models.expense import ExpenseModel
from src.models.category import CategoryModel
from src.models.user import UserModel
from marshmallow import fields

class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    category_name = fields.Method("get_category_name_by_id")
    username = fields.Method("get_username_by_id")
    class Meta:
        model = ExpenseModel
        load_instance = True
        include_fk = True
        dump_only = ("id",)
        load_only = ("category_id","user_id")
        fields = ("name","description","amount","category_id","user_id","category_name","username")

    def get_category_name_by_id(self,obj):
        return CategoryModel.find_category_by_id(obj.category_id).name

    def get_username_by_id(self, obj):
        return UserModel.find_by_id(obj.user_id).username


    
