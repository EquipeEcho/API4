from src.models.user import User

def test_create_user(teste_db):
    username = 'usuario_teste'
    test_email = 'usuario@email.com'
    test_password_unhashed = 'senha_secreta_123'
    user = User(name=username, email=test_email, password=test_password_unhashed)
    teste_db.add(user)
    teste_db.flush(user)


    

