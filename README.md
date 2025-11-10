# 🤖 Agente de Suporte com IA (Projeto `agentesuporte`)

Este projeto implementa um sistema de agente de suporte ao cliente utilizando uma arquitetura de múltiplos agentes. A aplicação é construída em Python com **FastAPI** e utiliza a **API Google Generative AI (Gemini)** para processamento de linguagem natural e tomada de decisão.

O fluxo de atendimento é dividido em agentes especializados:
* **Agente Inicial:** Faz a primeira triagem da solicitação do cliente.
* **Agente de Diagnóstico:** Coleta informações e utiliza as ferramentas (`services`) para diagnosticar o problema.
* **Agente de Escalonamento:** Decide se o caso precisa ser escalonado para um atendente humano.
* **Agente de Feedback:** Coleta o feedback do cliente ao final do atendimento.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI:** Para a criação da API web.
* **Uvicorn:** Como servidor ASGI para o FastAPI.
* **Google Generative AI (Gemini):** Para a inteligência dos agentes.
* **Pydantic:** Para validação de dados.
* **python-dotenv:** Para gerenciamento de variáveis de ambiente.

---

## 🚀 Como Começar

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Pré-requisitos

* Python 3.11 ou superior
* Git
* Uma API Key do Google AI Studio (para o Gemini)

### 2. Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/castello898/agentesuporte.git](https://github.com/castello898/agentesuporte.git)
    cd agentesuporte
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuração

Este projeto precisa de variáveis de ambiente para funcionar.

1.  Crie um arquivo chamado `.env` na raiz do projeto.
2.  Adicione as chaves necessárias. No mínimo, você precisará da sua chave da API do Google.

    **Exemplo de `.env`:**
    ```dotenv
    # Chave da API do Google AI Studio (Gemini)
    GOOGLE_API_KEY="SUA_API_KEY_AQUI"
    
    # Adicione outras chaves que seus serviços possam precisar
    # (Ex: URLs de CRM, tokens de API de frete, etc.)
    CRM_API_URL="[https://api.exemplo.com/crm](https://api.exemplo.com/crm)"
    SHIPPING_API_TOKEN="seu_token_secreto"
    ```
    
    > **Nota:** O arquivo `.env` está corretamente listado no seu `.gitignore`, garantindo que suas chaves secretas não sejam enviadas para o GitHub.

### 4. Executando a Aplicação

Com o ambiente ativado e o `.env` configurado, inicie o servidor FastAPI:

```bash
uvicorn main:app --reload

O servidor estará disponível em: http://127.0.0.1:8000

JSON

{
  "session_id": "user_session_abc123",
  "message": "Olá, meu pedido #12345 está atrasado. Pode verificar?"
}