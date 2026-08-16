from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Models need to be imported here to be registered
        from models.produto import Produto
        from models.usuario import Usuario
        from models.pedido import Pedido, ItemPedido
        db.create_all()
