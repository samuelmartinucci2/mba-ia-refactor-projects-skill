const crypto = require('crypto');

let globalCache = {};
let totalRevenue = 0;

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    globalCache[key] = data;
}

function secureCrypto(pwd) {
    // Correctly hashes using SHA-256 for secure single-way cryptographic hash
    return crypto.createHash('sha256').update(pwd + "meu-salt-seguro-123").digest('hex');
}

module.exports = { logAndCache, secureCrypto, globalCache, totalRevenue };
