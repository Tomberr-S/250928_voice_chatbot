from google.cloud import speech, texttospeech
import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)

# Google Cloudの認証情報を設定
PROJECT_ID = *****
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""
        あなたは有能なアシスタントです。ユーザーの質問に対して、正確かつ簡潔に答えてください。ただし、箇条書きで答えることは**絶対に**避けてください。
        """,
    )

client = speech.SpeechClient() # Speech-to-Textクライアントの初期化
client_voice = texttospeech.TextToSpeechClient() # Text-to-Speechクライアントの初期化

def transcribe_gcs_audio(content: str) -> speech.RecognizeResponse:
    """
    音声をSpeech-to-text APIを使って、テキストに変換
    """
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2, # WAVヘッダーに記載されているチャンネル数を指定
        enable_separate_recognition_per_channel=True, # チャンネルごとに個別に認識を有効にする
        sample_rate_hertz=16000,
        language_code="ja-JP",
        enable_automatic_punctuation=True,  # 句読点を自動付与する
    )

    # Performs synchronous speech recognition on the audio file
    print("Transcribing audio...")
    response = client.recognize(config=config, audio=audio)
    print(response)
    # Print the transcription
    transcript = ""
    for result in response.results:
        transcript = result.alternatives[0].transcript
        print(f"Transcript: {result.alternatives[0].transcript}")

    return transcript


def generate_response(prompt: str) -> str:
    """
    Geminiを使って、チャットの返答テキストを取得
    """
    print(prompt)
    response = model.generate_content(
        contents=[prompt],
        generation_config=GenerationConfig(
            temperature=0.2,
            max_output_tokens=1024,
            top_p=0.8,
            top_k=40
            )
        )
    
    reply = response.text

    return reply

def text_to_speech_and_play(text: str) -> bytes:
    """
    テキストをText-to-Speech APIを使って、音声に変換
    """
    # 入力テキストの設定
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 音声の設定（日本語、ニュートラルな声）
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    # オーディオ設定（MP3形式）
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    # 音声合成リクエスト
    response = client_voice.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content


