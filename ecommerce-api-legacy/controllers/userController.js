const UserModel = require('../models/userModel');

const deleteUser = async (req, res, next) => {
    try {
        const id = req.params.id;
        await UserModel.delete(id);
        
        return res.status(200).send("Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.");
    } catch (err) {
        next(err);
    }
};

module.exports = { deleteUser };
