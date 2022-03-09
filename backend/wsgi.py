from src.app import create_app
from src.db import db
from src.ma import ma
from src.blocklist import BLOCKLIST

app, jwt = create_app()

@app.before_first_request
def create_tables():
    db.create_all()

# This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

if __name__ =="__main__":
    app.run(debug=True)