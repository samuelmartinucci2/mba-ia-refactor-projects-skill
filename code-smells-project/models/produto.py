from database import get_db

class ProdutoModel:
    @staticmethod
    def get_todos():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM produtos")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "nome": row["nome"],
                "descricao": row["descricao"],
                "preco": row["preco"],
                "estoque": row["estoque"],
                "categoria": row["categoria"],
                "ativo": row["ativo"],
                "criado_em": row["criado_em"]
            })
        return result

    @staticmethod
    def get_por_id(id):
        db = get_db()
        cursor = db.cursor()
        # Parameterized Query
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "nome": row["nome"],
                "descricao": row["descricao"],
                "preco": row["preco"],
                "estoque": row["estoque"],
                "categoria": row["categoria"],
                "ativo": row["ativo"],
                "criado_em": row["criado_em"]
            }
        return None

    @staticmethod
    def criar(nome, descricao, preco, estoque, categoria):
        db = get_db()
        cursor = db.cursor()
        # Parameterized Query
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
            (nome, descricao, preco, estoque, categoria)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def atualizar(id, nome, descricao, preco, estoque, categoria):
        db = get_db()
        cursor = db.cursor()
        # Parameterized Query
        cursor.execute(
            "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
            (nome, descricao, preco, estoque, categoria, id)
        )
        db.commit()
        return True

    @staticmethod
    def deletar(id):
        db = get_db()
        cursor = db.cursor()
        # Parameterized Query
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
        db.commit()
        return True

    @staticmethod
    def buscar(termo, categoria=None, preco_min=None, preco_max=None):
        db = get_db()
        cursor = db.cursor()

        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        if termo:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            params.append(f"%{termo}%")
            params.append(f"%{termo}%")
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if preco_min:
            query += " AND preco >= ?"
            params.append(preco_min)
        if preco_max:
            query += " AND preco <= ?"
            params.append(preco_max)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "nome": row["nome"],
                "descricao": row["descricao"],
                "preco": row["preco"],
                "estoque": row["estoque"],
                "categoria": row["categoria"],
                "ativo": row["ativo"],
                "criado_em": row["criado_em"]
            })
        return result
