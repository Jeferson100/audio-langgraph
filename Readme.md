# Audio LangGraph

Este projeto explora a integração do processamento de áudio com LangGraph, uma biblioteca para construir aplicações robustas e com estado, multi-agentes, utilizando Large Language Models (LLMs). O objetivo é criar aplicações interativas que possam processar entrada de áudio e aproveitar LLMs para diversas tarefas.

## Funcionalidades

-   **Processamento de Áudio:** Lida com entrada de áudio (ex: gravação, transcrição).
-   **Integração LangGraph:** Utiliza LangGraph para definir e gerenciar fluxos de conversação complexos e comportamentos de agentes.
-   **Notebooks Interativos:** Notebooks Jupyter (`audio_langgraph.ipynb`, `audio_ux.ipynb`) para experimentação, desenvolvimento e demonstração de funcionalidades.
-   **Gerenciamento de Estado LangGraph:** `langgraph.json` provavelmente armazena definições de grafo ou estado.
-   **Testes/Exemplos:** `teste_langgraph.py` fornece exemplos ou testes para a implementação do LangGraph.

## Configuração

Para configurar o projeto, siga estes passos:

1.  **Navegue até o diretório do projeto:**
    ```bash
    cd audio-langgraph
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv .venv
    ```

3.  **Ative o ambiente virtual:**
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Notebooks Jupyter

Explore os notebooks interativos para entender e executar os diferentes componentes do projeto:

*   `audio_langgraph.ipynb`: Notebook principal demonstrando as funcionalidades centrais de áudio e LangGraph.
*   `audio_ux.ipynb`: Foca nos aspectos de experiência do usuário relacionados à interação de áudio.

Para executar os notebooks, certifique-se de ter o Jupyter instalado (`pip install jupyter`) e, em seguida, execute:
```bash
jupyter notebook
```
Navegue até os respectivos arquivos `.ipynb`.

### Scripts Python

*   `teste_langgraph.py`: Contém exemplos de uso ou testes para a implementação do LangGraph. Você pode executá-lo diretamente:
    ```bash
    python teste_langgraph.py
    ```

### Streamlit App

O projeto inclui uma aplicação web interativa construída com Streamlit.

*   `audio_streamlit.py`: Uma aplicação de chat que permite aos usuários interagir com um assistente de IA usando tanto texto quanto entrada de áudio. A aplicação transcreve o áudio do usuário, envia para um modelo de linguagem e converte a resposta do modelo em áudio.

Para executar a aplicação Streamlit, execute o seguinte comando no seu terminal:

```bash
streamlit run audio_streamlit.py
```

## Variáveis de Ambiente

Variáveis de ambiente ou chaves de API podem ser necessárias para certas funcionalidades (ex: chaves de API de LLM). Consulte o arquivo `.env` (se presente) ou os notebooks/scripts para detalhes de configuração específicos.
