================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   3 analyzed | ~400 lines of code

## Summary
CRITICAL: 3 | HIGH: 0 | MEDIUM: 1 | LOW: 1

## Findings

### [CRITICAL] Callback Hell / Pyramid of Doom
- **File:** src/AppManager.js:90-130
- **Description:** A rota `/api/checkout` contém um profundo aninhamento lateral de funções de callback para queries SQLite sequenciais (selecionar usuário, inserir matrícula, inserir pagamento).
- **Impact:** Código extremamente difícil de manter, depurar e testar. Qualquer erro no meio das transações é de difícil captura, o que pode causar inconsistências financeiras graves (como criar matrícula sem pagamento).
- **Recommendation:** Refatorar o driver de banco de dados para utilizar Promises e reescrever a rota utilizando a sintaxe limpa e legível de `async/await`.

### [CRITICAL] Insecure Password Hashing (Falsa Criptografia)
- **File:** src/utils.js:15-22
- **Description:** A função `badCrypto` simula hashing de senha aplicando codificação Base64 repetitivamente em um loop de 10000 iterações.
- **Impact:** Base64 é um algoritmo bidirecional e perfeitamente reversível, não um hash seguro de via única. As senhas dos alunos ficam expostas no banco de dados, violando políticas básicas de segurança.
- **Recommendation:** Substituir o uso de Base64 pelo módulo de criptografia nativo do Node.js (`crypto`), aplicando por exemplo o algoritmo seguro `SHA-256` com salt ou usando `bcrypt`.

### [CRITICAL] Hardcoded Credentials (Segredos no Código)
- **File:** src/utils.js:1-7
- **Description:** O arquivo centraliza segredos confidenciais em texto claro, incluindo chaves do gateway de pagamento em ambiente de produção (`paymentGatewayKey: "pk_live_1234567890abcdef"`) e senhas do banco de dados.
- **Impact:** Exposição grave de dados financeiros e infraestrutura de produção caso o código seja versionado em repositórios públicos.
- **Recommendation:** Extrair todas as credenciais sensíveis e chaves de APIs para variáveis de ambiente utilizando o arquivo `.env` e carregando-as com `process.env`.

### [MEDIUM] Query N+1 no Banco de Dados
- **File:** src/AppManager.js:140-185
- **Description:** O endpoint de relatório financeiro `/api/admin/financial-report` executa queries consecutivas no banco para cada curso, matrícula e aluno de forma síncrona dentro de loops `forEach`.
- **Impact:** Overhead massivo de chamadas I/O ao banco de dados que degrada de forma exponencial a performance e escalabilidade do servidor conforme o volume de alunos e cursos cresce.
- **Recommendation:** Reescrever a agregação utilizando uma única consulta SQL otimizada com cláusulas `JOIN` (`courses JOIN enrollments JOIN payments JOIN users`) trazendo os dados consolidados.

### [LOW] Nomenclatura Pobre de Variáveis
- **File:** src/AppManager.js:92-96
- **Description:** Uso de variáveis com nomes curtos e sem significado contextual, como `let u` para usuário, `let e` para email e `let p` para senha na requisição de checkout.
- **Impact:** Prejuízo na legibilidade do código e aumento do tempo de onboarding para novos desenvolvedores na codebase.
- **Recommendation:** Adotar nomenclatura descritiva de variáveis de acordo com as boas práticas de Clean Code (ex: `username`, `email`, `password`).

================================
Total: 5 findings
================================
