# coding: utf-8
import streamlit as st
import hashlib
import openai 
from streamlit_chat import message

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def login_user(username, password):
    if username == st.secrets["user"] and password == st.secrets["password"]:
        return True
    else:
        return False

def chat():
    openai.api_key  = st.secrets["API_key"]

    def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"]
    
    menu = f"""
    ハンバーガー 550円
    """

    context = [ {'role':'system', 'content':"""
    You are question answering bot, an automated service to aswer to customer's question about menu. \
    You first greet the customer in short, then answer to the question, \
    Make sure to clarify all options, extras and concentration to uniquely \
    identify the item from the menu.\
    You respond in a short, very conversational friendly style. \
    Translate them to Japanese. \
    The menu includes below. \
    """ + menu} ]

    # 初めてのセッションの場合、コンテキストの初期化
    if 'context' not in st.session_state:
        st.session_state["context"] = context

    # ボタンを押した場合、コンテキストの初期化
    if st.button("最初からやり直す"):
        st.session_state["context"] = context

    # テキストインプット
    def get_text():
        input_text = st.text_input("あなた: ","", key = "input")
        return input_text

    # コンテキストから回答を生成
    user_input = get_text()
    if user_input:
        context = st.session_state["context"]
        context.append({'role':'user', 'content':f"{user_input}"})
        response = get_completion_from_messages(context) 
        context.append({'role':'assistant', 'content':f"{response}"})
        st.session_state["context"] = context

    # チャット内容の表示
    for i, c in enumerate(reversed(context[1:])):
        message(c["content"], is_user = (i % 2 == 1), key = str(i) + c["role"])

def main():
#    username = st.sidebar.text_input("ユーザー名を入力してください")
#    password = st.sidebar.text_input("パスワードを入力してください", type = "password")
#    if st.sidebar.checkbox("ログイン"):
#        hashed_pswd = make_hashes(password)
#        result = login_user(username,check_hashes(password,hashed_pswd))
#        if result:
#            chat()
#        else:
#            st.warning("ユーザー名かパスワードが間違っています")
    chat()

if __name__ == "__main__":
    main()