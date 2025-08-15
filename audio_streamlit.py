import os
import streamlit as st
from streamlit_chat_widget import chat_input_widget
from streamlit_float import * 
from groq import Groq
from dotenv import load_dotenv
from langchain_groq import ChatGroq
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play
    ELEVENLABS_AVAILABLE = True
except ImportError:
    print("ElevenLabs not available, using Groq TTS only")
    ELEVENLABS_AVAILABLE = False
import sounddevice as sd
from scipy.io.wavfile import write, read
import tempfile
from audio_langgraph import graph_builder
from contextlib import contextmanager
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    SystemMessage
)
from langchain_core.output_parsers import StrOutputParser


st.set_page_config(
    page_title="Bot Assistente com Audio",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Agente com audio",
    },
)

load_dotenv()

@contextmanager
def temp_env_vars(**kwargs):
    """
    Context manager que cria variáveis de ambiente temporárias.
    Restaura os valores originais ao sair do contexto.
    """
    # Salva valores originais
    original_values = {}
    for key in kwargs:
        original_values[key] = os.environ.get(key)

    # Define novos valores
    for key, value in kwargs.items():
        if value is not None:
            os.environ[key] = str(value)
        elif key in os.environ:
            del os.environ[key]

    try:
        yield
    finally:
        # Restaura valores originais
        for key, original_value in original_values.items():
            if original_value is not None:
                os.environ[key] = original_value
            elif key in os.environ:
                del os.environ[key]


if (
    "groq_api" in st.session_state
    and st.session_state.groq_api
    or os.getenv("GROQ_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API do GROQ.")

if (
    "elevenlabs_api" in st.session_state
    and st.session_state.elevenlabs_api
    or os.getenv("ELEVENLABS_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API do ElevenLabs.")

if ELEVENLABS_AVAILABLE:
    elevenlabs = ElevenLabs(
      api_key=st.session_state.elevenlabs_api if "elevenlabs_api" in st.session_state else os.getenv("ELEVENLABS_API_KEY"),
    )
else:
    elevenlabs = None

client = Groq()

chat = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,)

prompt_tradutor = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="""You are a helpful assistant that translates text from English to Portuguese.
            Your task is to translate the entire {input} into natural, fluent Portuguese.
            Do not answer questions or provide explanations in English — only translate the given text."""),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

chat_tradutor = prompt_tradutor | chat | StrOutputParser()

graph = graph_builder().compile()


def play_audio(texto_input):
    """Plays the audio response using Groq TTS."""
    
    # Prepare text by replacing ** with empty strings
    # These can cause unexpected behavior in TTS
    if isinstance(texto_input, str):
        cleaned_text = texto_input.replace("**", "")
    else:
        cleaned_text = texto_input.content.replace("**", "")

    if ELEVENLABS_AVAILABLE and elevenlabs:
        try:
            audio = elevenlabs.text_to_speech.convert(
                text=cleaned_text,
                #voice_id="JBFqnCBsd6RMkjVDRZzb",
                #model_id="eleven_multilingual_v2",
                #voice_id="GnDrTQvdzZ7wqAKfLzVQ",
                #voice_id = "8ydzsJeYlXGq5mRMX93B",
                voice_id="EIkHVdkuarjkYUyMnoes",
                
                model_id="eleven_multilingual_v1",
                output_format="mp3_44100_128",
            )
            play(audio)
            return
        except Exception as e:
            print(f"Error in elevenlabs: {e}")
            try:
                # Call Groq text-to-speech API
                tts_response = client.audio.speech.create(
                    model="playai-tts",
                    voice="Arista-PlayAI",
                    input=cleaned_text,
                    response_format="wav"
                )
                
                # Create temporary file and read audio data
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    tts_response.write_to_file(temp_file.name)
                    temp_audio_file = temp_file.name
                
                # Read the WAV file and play with sounddevice
                sample_rate, audio_data = read(temp_audio_file)
                sd.play(audio_data, sample_rate)
                sd.wait()  # Wait until the audio finishes playing
                
            except Exception as e:
                print(f"Error in text-to-speech: {e}")
            finally:
                # Clean up
                if 'temp_audio_file' in locals():
                    try:
                        os.unlink(temp_audio_file)
                    except:
                        pass

def app():
    st.title("Assistant Chat com Audio")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    messages = st.session_state.chat_history

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display the chat input widget at the bottom
    #user_input = chat_input_widget()
    
    float_init()
    footer_container = st.container()
    with footer_container:
        user_input = chat_input_widget()

    with st.sidebar:
        st.write("## Instruções")
        st.write("Esse é um assistente que tem como caracteristicas o uso da voz para interação com o usuário.")
       
        
        st.markdown("# Login APIS:")
        st.write(
            """Para utilizar o Bot, primeiro faça o cadastro gratuito nos site abaixo e 
            depois gere as chaves API necessária:"""
        )

        st.markdown(
            """
        [![Groq API](https://img.shields.io/badge/Create%20Groq%20API%20Key-black?style=flat&logo=groq)](https://console.groq.com/keys)
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        [![ElevenLabs API](https://img.shields.io/badge/Create%20ElevenLabs%20API%20Key-blue?style=flat&logo=groq)](https://elevenlabs.io/app/settings/api-keys)
        """,
            unsafe_allow_html=True,
        )

        if "groq_api" not in st.session_state:
            st.session_state["groq_api"] = None

        if "elevenlabs_api" not in st.session_state:
            st.session_state["elevenlabs_api"] = None

        try:
            if os.getenv("GROQ_API_KEY") is not None:
                groq_api = os.getenv("GROQ_API_KEY")
                st.success("API key GROQ ja existe!", icon="✅")
            else:
                # Pede a chave apenas se ainda não estiver salva
                api_key = st.text_input(
                    "Enter GROQ API token:",
                    value=st.session_state.groq_api,
                    type="password",
                )

                if api_key:
                    st.session_state.groq_api = api_key
                    st.success("API key GROQ configurada com sucesso!", icon="✅")

            if os.getenv("ELEVENLABS_API_KEY") is not None:
                elevenlabs_api = os.getenv("ELEVENLABS_API_KEY")
                st.success("API key ELEVENLABS ja existe!", icon="✅")

            else:
                # Pede a chave apenas se ainda não estiver salva
                elevenlabs_api = st.text_input(
                    "Enter ELEVENLABS API token:",
                    value=st.session_state.elevenlabs_api,
                    type="password",
                )

                if elevenlabs_api:
                    st.session_state.elevenlabs_api = elevenlabs_api
                    st.success("API key ELEVENLABS configurada com sucesso!", icon="✅")

        except ValueError as e:
            st.error(f"Erro ao utilizar a API: {e}")
            st.stop()
            
        
    if user_input:
        if "text" in user_input:
            user_text =user_input["text"]
            user_text = chat_tradutor.invoke({"input": user_text})
            messages.append({"role": "user", "content": user_text})
            #st.session_state.chat_history.append(user_text)
            #response = chat_prompt.invoke({"input": user_text})
            response = graph.invoke({"messages": user_text})
            if isinstance(response["messages"][-1], str):
                print(response["messages"][-1])
                response = response["messages"][-1]
            else:
                print(response["messages"][-1].content)
                response = response["messages"][-1].content
                
            play_audio(response)
            with st.chat_message("assistant"):
                st.write(response)
            messages.append({"role": "assistant", "content": response})
            
        elif "audioFile" in user_input:
            audio_bytes = bytes(user_input["audioFile"])
            translation = client.audio.translations.create(
                file=("speech.wav", audio_bytes), 
                model="whisper-large-v3", 
                prompt="Transcreva o áudio em português brasileiro", 
                #language="br",
                response_format="json",
                temperature=0.0
                )
            translation = chat_tradutor.invoke({"input": translation.text})
            messages.append({"role": "user", "content": translation})
            #response = chat_prompt.invoke({"input": translation.text})
            response = graph.invoke({"messages": translation})
            if isinstance(response["messages"][-1], str):
                print(response["messages"][-1])
                response = response["messages"][-1]
            else:
                print(response["messages"][-1].content)
                response = response["messages"][-1].content
            play_audio(response)
            with st.chat_message("assistant"):
                st.write(response)
            messages.append({"role": "assistant", "content": response})
        
if __name__ == "__main__":
    app()