import os
import streamlit as st
from streamlit_chat import message
import openai



# APIキーの取得
openai_api_key = os.environ.get('OPENAI_API_KEY')
# APIキーの設定
openai.api_key = openai_api_key

# 「送信」ボタンがクリックされた場合に、OpenAIに問い合わせる
def do_question():
    condition = st.session_state.condition_input.strip()
    if condition and condition != st.session_state.condition:
        st.session_state.condition = condition
        st.session_state.messages.append({"role": "system", "content": condition})

    question = st.session_state.question_input.strip()
    if question:
        #メッセージに質問を追加
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.question_input = ""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        
        message = response.choices[0]["message"]
        #回答をメッセージに追加
        st.session_state.messages.append(message)

def main():
    # セッションステートに messages リストを初期化する
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.condition = ""

    #タイトル
    st.title("GPTチャット！")
    # テキストボックスに役割を入力
    st.text_input("（任意）人物設定してください。(例:「あなたはいけずな京都人です。京都弁で話してください。」)", key="condition_input")
    # テキストボックスで質問を入力
    st.text_input("（必須）質問を入力してください", key="question_input")
    # 送信ボタンがクリックするとOpenAIに問い合わせる
    st.button("送信", on_click=do_question)

    # messagesをループして、質問と回答を表示
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        #右側に表示する回答はisUserをTrueとする。
        message((msg["content"]), is_user = msg["role"] == "assistant") 

if __name__ == "__main__":
    main()  