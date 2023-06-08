# Api para transações bancárias

# Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/dasilvactu/condotest.git

2. Instale as depenências
   ```bash
   pip install -r requirements.txt
## Endpoints

### Consultar Saldo

- Método: GET
- URL: `/saldo`
- Descrição: Permite consultar o saldo de uma conta bancária específica.
- Parâmetros:
  - `conta_id` (obrigatório): ID da conta bancária a ser consultada.
  - `tipo` (obrigatório): Tipo da conta bancária a ser consultada. Deve ser "conta_corrente" ou "conta_poupanca".
- Respostas:
  - 200 OK: A requisição foi bem-sucedida. A resposta JSON contém o saldo da conta consultada.
  - 400 Bad Request: A requisição está incorreta ou faltam parâmetros obrigatórios. A resposta JSON contém uma mensagem de erro.
  - 404 Not Found: A conta bancária não foi encontrada. A resposta JSON contém uma mensagem de erro.

### Consultar extrato mês corrente
 - Método: GET
 - URL: `/extrato`
 - Descrição: Esta rota permite consultar o extrato de uma conta específica para o mês corrente.
 - Parâmetros:
    - `conta_id` (obrigatório) - ID da conta para a qual o extrato será consultado.
    - `tipo` (obrigatório) - `conta_corrente`| `conta_poupanca` 
 - Respostas :
  - 200 OK: A requisição foi bem-sucedida. A resposta JSON contém o saldo da conta consultada.
  - 400 Bad Request: A requisição está incorreta ou faltam parâmetros obrigatórios. A resposta JSON contém uma mensagem de erro.
  - 404 Not Found: A conta bancária não foi encontrada. A resposta JSON contém uma mensagem de erro.

### Transferência entre contas
 - Método: POST
 - URL: `/transferencia`
 - Descrição: Esta rota permite transferir fundos de uma conta corrente para poupança e vice e versa.
 - Parâmetros do corpo da solicitação:
  - `conta` (obrigatório) - ID da conta de origem da transferência.
  - `tipo_conta_destino` (obrigatório) - tipo conta destino : `conta_corrente`| `conta_poupanca` .
  - valor (obrigatório) - Valor a ser transferido.
- Respostas :
  - 200 OK: A requisição foi bem-sucedida. A resposta JSON contém o saldo da conta consultada.
  - 400 Bad Request: A requisição está incorreta ou faltam parâmetros obrigatórios. A resposta JSON contém uma mensagem de erro.
  - 404 Not Found: A conta bancária não foi encontrada. A resposta JSON contém uma mensagem de erro.

3. Testes
 - Todos os testes estão no arquivo teste_api.py e pode ser rodados usando o comando 
    ```bash
   python test_api.py
 - É necessário que a api esteja funcionando, para isso, rode o comando em um terminal
     ```bash
   flask run