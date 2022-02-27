from src.app import app 
from src.db import db
from src.ma import ma
from src.blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

# This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

if __name__ =="__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)