class Config:
    SECRET_KEY = 'ALURA'
    SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'jogoteca'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False