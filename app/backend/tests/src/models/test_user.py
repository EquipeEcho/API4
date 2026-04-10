from sqlalchemy import select
from src.models.user import User

def test_create_user(test_db):
    # --- ARRANGE (Preparação) ---
    test_name = 'usuario_teste'
    test_email = 'usuario@email.com'
    test_pass = 'senha_secreta_123'
    
    user = User(name=test_name, email=test_email, password=test_pass)
    
    # --- ACT (Ação) ---
    test_db.add(user)
    test_db.flush() 

    # Buscando o usuário recém-criado
    query = select(User).where(User.email == test_email)
    user_db = test_db.execute(query).scalar_one()

    # --- ASSERT (Verificação) ---
    assert user_db.name == test_name
    assert user_db.email == test_email
    assert user_db.id is not None  # Garante que o ID foi gerado pelo banco
    
    # Opcional: Se você estiver usando Pytest, pode imprimir para conferir no log
    print(f"Usuário {user_db.name} criado com ID {user_db.id}")