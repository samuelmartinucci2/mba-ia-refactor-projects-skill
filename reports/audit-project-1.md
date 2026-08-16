================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 1 | LOW: 1

## Findings

### [CRITICAL] SQL Injection Vulnerability
- **File:** models.py:20-450
- **Description:** A aplicação utiliza concatenação direta de strings e variáveis para construir e executar instruções SQL no banco de dados SQLite.
- **Impact:** Permite que atacantes maliciosos executem queries arbitrárias no banco de dados, facilitando o roubo, alteração ou exclusão de dados e bypass completo de mecanismos de autenticação (como na função login_usuario).
- **Recommendation:** Substituir todas as concatenações de strings SQL pelo uso correto de placeholders parametrizados (ex: `cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))`).

### [CRITICAL] God Class / God Module (Módulo Único de Persistência e Domínio)
- **File:** models.py:1-450
- **Description:** O arquivo models.py acumula toda a infraestrutura de dados, queries brutas e regras de negócio de múltiplos domínios (Produtos, Usuários, Pedidos).
- **Impact:** Altíssimo acoplamento entre os domínios da aplicação, tornando impossível realizar testes unitários isolados ou escalar/alterar um domínio sem o risco de corromper os outros.
- **Recommendation:** Reestruturar e dividir o arquivo em models isolados por domínio, de acordo com o padrão MVC (ex: `models/produto.py`, `models/usuario.py`, `models/pedido.py`), desacoplando as operações do banco.

### [HIGH] Hardcoded Credentials (Segredos Sensíveis Expostos)
- **File:** app.py:8-8
- **Description:** A chave secreta de criptografia da aplicação (`app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"`) está exposta em texto claro no código de inicialização do servidor.
- **Impact:** Permite o comprometimento e falsificação das sessões e cookies dos usuários caso o código seja publicado em repositórios de controle de versão.
- **Recommendation:** Utilizar a biblioteca `python-dotenv` para carregar a `SECRET_KEY` de variáveis de ambiente do sistema, fornecendo apenas um fallback padrão de desenvolvimento.

### [HIGH] Lógica de Negócio Acoplada no Controller (Fat Controller / Orquestração)
- **File:** controllers.py:206-239
- **Description:** A função `criar_pedido` executa regras de negócio pesadas (verificação manual de estoque para cada item de produto, atualização direta do banco e orquestração de notificações impressas).
- **Impact:** Impede a reutilização destas lógicas em outros canais (como comandos CLI ou processos agendados) e viola os limites arquiteturais do padrão MVC.
- **Recommendation:** Mover a lógica de orquestração de pedidos, validação de estoque e transações para um Service ou para os respectivos Models puros, deixando o controller responsável apenas pelo fluxo HTTP.

### [MEDIUM] Endpoints Administrativos Inseguros (Raw SQL)
- **File:** app.py:46-77
- **Description:** Os caminhos de URL `/admin/reset-db` e `/admin/query` estão expostos publicamente e permitem, respectivamente, apagar todas as tabelas e executar qualquer query arbitrária enviada no corpo da requisição.
- **Impact:** Risco gravíssimo de destruição ou vazamento completo de dados por qualquer cliente sem privilégios administrativos.
- **Recommendation:** Remover o endpoint de consulta SQL arbitrária em produção e implementar autenticação/autorização robusta baseada em middleware (ex: JWT Admin) nas rotas administrativas.

### [LOW] Uso de Print como Logger e Print de Exceções Sem Stack Trace
- **File:** controllers.py:1-255
- **Description:** Mensagens de erro e debug são logadas diretamente para a saída padrão (`stdout`) utilizando `print()` em vez de um logger estruturado do Python.
- **Impact:** Dificulta a filtragem e monitoramento de falhas estruturadas em ambiente de produção (por exemplo, utilizando agregadores de log como Datadog ou Splunk).
- **Recommendation:** Configurar o módulo nativo de `logging` do Python para formatar logs de erro adequadamente, contendo nível, timestamp e stacktrace em canais apropriados.

================================
Total: 6 findings
================================
