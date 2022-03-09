from src.models.user import UserModel

def test_user(new_user):
    '''
    GIVEN a User model
    WHEN a new user is created
    THEN check the username and password are defined correctly
    '''
    # user = UserModel(username = "Username",password = "Password")
    assert new_user.username == "Username"
    assert new_user.password == "password"