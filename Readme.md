# Chatbot com LangGraph e Groq

Este projeto demonstra a criação de um agente de conversação simples utilizando a biblioteca LangGraph para orquestrar o fluxo, com o poder do modelo de linguagem da Groq para respostas rápidas.

## Funcionalidades

- **Agente Conversacional**: Responde a perguntas em português.
- **Orquestração com LangGraph**: Utiliza um grafo de estados para gerenciar a conversa.
- **LLM Rápido**: Integra-se com a API da Groq para inferência de alta velocidade.
2.
- **Gerenciamento de Dependências**: Inclui um arquivo `requirements.txt` para fácil instalação.
- **Configuração de Ambiente**: Usa um arquivo `.env` para gerenciar chaves de API de forma segura.

## Pré-requisitos

- Python 3.9 ou superior
- Uma chave de API da Groq
- Uma chave de API do ElevenLabs

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Jeferson100/audio-langgraph.git
    cd audio-langgraph
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv .venv

    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas chaves de API:**
    - Renomeie o arquivo `.env.example` para `.env`.
    - Adicione sua chave de API da Groq ao arquivo `.env`:
      ```env
      GROQ_API_KEY="sua_chave_aqui"
      ELEVENLABS_API_KEY="sua_chave_aqui" # Para uso futuro com ElevenLabs
      ```

## Como Usar

Este projeto pode ser executado de duas maneiras: atraves do notebook `audio_langgraph.ipynb` ou como uma aplicação web interativa com Streamlit.

### 1. Executando o Notebook

Para testar o agente use o notebook `audio_langgraph.ipynb`.

### 2. Executando a Aplicação Web (Streamlit)

Para uma experiência de chat interativa, inicie a aplicação Streamlit.

```bash
streamlit run audio_streamlit.py
```
Após executar o comando, uma nova aba será aberta no seu navegador com a interface do chatbot.
