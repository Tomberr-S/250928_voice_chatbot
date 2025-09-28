import time
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64
import time

from llm import generate_response, transcribe_gcs_audio, text_to_speech_and_play

# Streamlitのページ設定
st.set_page_config(
    page_title="dev VoiceChat",
    page_icon=":robot_face:",
    layout="wide"
)

st.title("Voice Chat with Gemini")

# 音声入力の録音UI
def ui():
    # マイク入力
    audio_bytes = audio_recorder(
        text="音声で入力したい場合はこちらをクリック！",
        pause_threshold=30,
        sample_rate=16000,
        ) # sample_rateを16000Hzに設定 (Google Speech-to-Textの推奨値)
    
    # audio_bytes = st.audio_input("Record a voice message")
    st.markdown("---")

    # 初期表示時のメッセージ
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # チャット履歴の表示
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    # 音声入力時の処理
    if st.button("Start"):
        if audio_bytes:
        # 音声入力のテキスト変換
            transcript = transcribe_gcs_audio(audio_bytes)
            st.session_state["messages"].append({"role": "user", "content": transcript})
            st.chat_message("user").write(transcript)

            # 音声合成を使用してAIの返答を表示しながら読み上げる
            reply = generate_response(transcript)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            last_message = st.session_state["messages"][-1]
            if last_message["role"] == "assistant":
                # AIの返答を読み上げ
                voice_read = text_to_speech_and_play(last_message["content"])
                # 音声を直接再生
                # st.audio(voice_read, format="audio/mp3")
                audio_str = "data:audio/ogg;base64,%s"%(base64.b64encode(voice_read).decode())
                audio_html = """
                                <audio autoplay=True>
                                <source src="%s" type="audio/ogg" autoplay=True>
                                Your browser does not support the audio element.
                                </audio>
                            """ %audio_str
                
                audio_placeholder = st.empty()
                audio_placeholder.empty()
                time.sleep(0.5) #これがないと上手く再生されませんらしい
                audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

                st.chat_message("assistant").write(last_message["content"])

ui()
