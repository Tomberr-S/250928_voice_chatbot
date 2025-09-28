# 250928_voice_chatbot

このプロジェクトは、音声入力を受け取り、AIによる応答を生成し、その応答を音声で読み上げるデモアプリケーションです。

## 機能概要

1. **音声入力**:
   - ユーザーが音声を録音し、アプリケーションに送信します。
   - Google Cloud Speech-to-Text APIを使用して音声をテキストに変換します。

2. **AI応答生成**:
   - 変換されたテキストを基に、Google Cloud Vertex AIのGenerative Model（Gemini-2.0）を使用して応答を生成します。

3. **音声出力**:
   - 生成された応答をGoogle Cloud Text-to-Speech APIを使用して音声に変換し、再生します。

4. **インターフェース**:
   - Streamlitを使用したシンプルで直感的なWebインターフェースを提供します。

## 使用技術

- **プログラミング言語**: Python
- **主要ライブラリ**:
  - `google-cloud-speech`
  - `google-cloud-texttospeech`
  - `google-cloud-aiplatform`

- **その他**:
  - Google Cloud Platform（GCP）を利用した音声認識、音声合成、AIモデルのホスティング

## セットアップ手順

1. **必要なライブラリのインストール**:
   プロジェクトルートにある`requirements.txt`を使用して、必要なPythonライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```

2. **Google Cloudの設定**:
   - GCPプロジェクトを作成し、必要なAPI（Speech-to-Text, Text-to-Speech, Vertex AI）を有効化します。
   - ```gcloud auth application-default login```を実行してログインしてください。
   - ```PROJECT_ID```と```locate```を設定してください。

3. **アプリケーションの起動**:
   Streamlitを使用してアプリケーションを起動します。
   ```bash
   streamlit run streamlit.py
   ```

## ファイル構成

- `llm.py`: 音声認識、AI応答生成、音声合成のロジックを含むモジュール
- `streamlit.py`: ユーザーインターフェースを提供するStreamlitアプリケーション
- `requirements.txt`: 必要なPythonライブラリのリスト
- `README.md`: プロジェクトの概要とセットアップ手順

## デモの流れ

1. アプリケーションを起動し、音声入力を録音します。
2. 録音した音声がテキストに変換され、AIが応答を生成します。
3. 生成された応答が音声で再生されます。

## 注意事項

- このプロジェクトを実行するには、Google Cloudのアカウントと適切な設定が必要です。
- 音声データの取り扱いには十分注意し、プライバシーを保護してください。
