const crypto = require('crypto');

function secureCrypto(pwd) {
    // Correctly hashes using SHA-256 for secure single-way cryptographic hash
    return crypto.createHash('sha256').update(pwd + "meu-salt-seguro-123").digest('hex');
}

module.exports = { secureCrypto };
