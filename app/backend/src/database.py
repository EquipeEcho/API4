from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db') # Usando sqlite enquanto o SGBD não foi definido
# TODO: mudar a string de conexão pra Mysql ou PostGre
# postgresql+psycopg2://usuario:senha@db:5432/nome_do_banco
SessionLocal = sessionmaker(bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session