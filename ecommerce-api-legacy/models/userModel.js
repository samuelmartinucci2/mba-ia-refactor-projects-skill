const { dbGet, dbRun, dbAll } = require('../database');

class UserModel {
    static async getByEmail(email) {
        return await dbGet("SELECT * FROM users WHERE email = ?", [email]);
    }

    static async getById(id) {
        return await dbGet("SELECT id, name, email FROM users WHERE id = ?", [id]);
    }

    static async create(name, email, passwordHash) {
        const result = await dbRun(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, passwordHash]
        );
        return result.lastID;
    }

    static async delete(id) {
        return await dbRun("DELETE FROM users WHERE id = ?", [id]);
    }
}

module.exports = UserModel;
