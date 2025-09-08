# Walkie Backend

Este é o repositório do backend da aplicação Walkie, construído com Flask.

## Configuração do Ambiente

Certifique-se de ter Python 3.9+ e pip instalados.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/HaroldoNascimento/walkie2.git
    cd walkie2/dog-walker-backend
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Rodar a Aplicação

1.  **Defina as variáveis de ambiente (opcional, mas recomendado para produção):**
    ```bash
    export SECRET_KEY="sua_chave_secreta_aqui"
    export JWT_SECRET_KEY="sua_chave_jwt_secreta_aqui"
    ```
    Se não definir, chaves padrão serão usadas.

2.  **Execute a aplicação:**
    ```bash
    python src/main.py
    ```
    O servidor estará disponível em `http://0.0.0.0:5000`.

## Estrutura do Projeto

```
.dog-walker-backend/
├── Dockerfile
├── requirements.txt
└── src/
    ├── main.py
    ├── models/
    │   └── user.py
    └── routes/
        ├── auth.py
        ├── dogs.py
        └── walks.py
```

## Endpoints da API

-   `/api/health` (GET): Verifica o status do backend.
-   `/api/register` (POST): Registra um novo usuário.
-   `/api/login` (POST): Autentica um usuário e retorna um token JWT.
-   `/api/dogs` (GET, POST, PUT, DELETE): Gerencia os cães do usuário.
-   `/api/walks` (GET, POST, PUT): Gerencia os passeios dos cães.
-   `/api/walks/stats` (GET): Retorna estatísticas dos passeios.


