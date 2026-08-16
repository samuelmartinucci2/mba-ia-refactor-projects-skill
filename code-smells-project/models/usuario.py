from database import get_db

class UsuarioModel:
    @staticmethod
    def get_todos():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "nome": row["nome"],
                "email": row["email"],
                "senha": row["senha"],
                "tipo": row["tipo"],
                "criado_em": row["criado_em"]
            })
        return result

    @staticmethod
    def get_por_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "nome": row["nome"],
                "email": row["email"],
                "senha": row["senha"],
                "tipo": row["tipo"],
                "criado_em": row["criado_em"]
            }
        return None

    @staticmethod
    def login(email, senha):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "nome": row["nome"],
                "email": row["email"],
                "tipo": row["tipo"]
            }
        return None

    @staticmethod
    def criar(nome, email, senha, tipo="cliente"):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, tipo)
        )
        db.commit()
        return cursor.lastrowid
