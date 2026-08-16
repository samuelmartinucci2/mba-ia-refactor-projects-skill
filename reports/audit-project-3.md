================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask
Files:   10 analyzed | ~1200 lines of code

## Summary
CRITICAL: 1 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] Credenciais Hardcoded no Serviço de Notificação (SMTP)
- **File:** services/notification_service.py:8-10
- **Description:** A senha do e-mail de envio de notificações do sistema está declarada diretamente em texto claro dentro da classe `NotificationService` (`self.email_password = 'senha123'`).
- **Impact:** Vazamento gravíssimo de credenciais corporativas no controle de versão do repositório, permitindo que atacantes enviem spam ou tenham controle sobre o e-mail oficial de notificações.
- **Recommendation:** Mover a senha e as configurações de host e porta SMTP para variáveis de ambiente carregadas pelo módulo `os.getenv` de forma segura.

### [HIGH] Credenciais Hardcoded (Secret Key do Flask)
- **File:** app.py:14-14
- **Description:** A `SECRET_KEY` da aplicação está declarada diretamente como `'super-secret-key-123'` no arquivo principal do Flask.
- **Impact:** Expõe as assinaturas de cookies de sessão dos usuários, tornando possível que atacantes falsifiquem identidades ou executem sequestros de sessão.
- **Recommendation:** Carregar a `SECRET_KEY` de variáveis de ambiente com um fallback seguro apenas para desenvolvimento local.

### [HIGH] Regras de Negócio e Acúmulo de Lógicas nas Rotas (Fat Controllers)
- **File:** routes/report_routes.py:12-92
- **Description:** A rota `/reports/summary` concentra toda a lógica de compilação de relatórios, cálculos manuais de fuso horário, estatísticas de produtividade e filtragem consecutiva de banco de dados.
- **Impact:** Forte violação do padrão MVC. As lógicas de geração de relatórios de produtividade ficam presas na camada de apresentação HTTP, impedindo a reutilização delas e inviabilizando testes unitários sem levantar o app Flask.
- **Recommendation:** Extrair a lógica pesada de relatórios para uma camada dedicada de Service ou métodos estáticos dentro das classes de modelo apropriadas.

### [MEDIUM] Uso de API Deprecated (datetime.utcnow)
- **File:** models/task.py:12-14
- **Description:** O uso de `datetime.utcnow` para data padrão e validação de fuso horário em tarefas. Esta função está formalmente depreciada desde o Python 3.12.
- **Impact:** Incompatibilidade futura com versões recentes do interpretador Python e falta de informações explícitas de timezone em bancos de dados.
- **Recommendation:** Substituir por `datetime.now(timezone.utc)` importando o módulo nativo `timezone` para representar as datas com fuso horário de forma segura.

### [MEDIUM] Mascaramento de Erros por Tratamento de Exceção Genérico
- **File:** routes/user_routes.py:148-151
- **Description:** Uso de bloco `try ... except:` vazio capturando todas as exceções durante a atualização de usuários sem registrar os detalhes da falha.
- **Impact:** Mascara as falhas reais do banco de dados (ex: integridade, formato), retornando `Erro ao atualizar` para o cliente e ocultando o rastreio (stack trace) essencial para a depuração de desenvolvimento.
- **Recommendation:** Substituir capturas genéricas por tratamento de exceções específicas (como `SQLAlchemyError`) e registrar o erro original utilizando biblioteca de log apropriada.

### [LOW] Serialização Manual Redundante de Dados nas Rotas
- **File:** routes/user_routes.py:171-193
- **Description:** Reconstrução manual de estruturas de dicionários JSON para objetos Task de dentro da rota `/users/<id>/tasks` em vez de delegar ao método `.to_dict()` nativo do modelo.
- **Impact:** Duplicação de código de formatação e facilidade de introduzir inconsistências entre endpoints que deveriam retornar o mesmo formato de dados.
- **Recommendation:** Utilizar consistentemente o método `.to_dict()` do próprio modelo Task ou criar um serializer adequado para centralizar a apresentação de dados.

================================
Total: 6 findings
================================
