from src.app import app 
from src.ma import ma
from src.db import db


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ =="__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)