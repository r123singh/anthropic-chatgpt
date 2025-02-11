import streamlit as st 
import anthropic
import os


def chat_screen():
    model = anthropic.Anthropic()
    st.title("🦾 Anthropic ChatGPT")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    def anthropic_invoke(user_query):
        response = model.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens = 1024,
            messages=[
                {
                    "role":"user",
                    "content": user_query
                }
            ]
        )
        with st.chat_message("assistant"):st.markdown(response.content[0].text)
        st.session_state.messages.append(
            {
            "role": "user",
            "content": user_query
            }
        )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response.content[0].text
            }
        )      
    user_query = st.chat_input("Message Anthropic GPT")

    if user_query:
        with st.chat_message("user"): st.markdown(user_query)
        anthropic_invoke(user_query)
    
    
def api_screen():
    st.title("🚀Welcome to AnthropicGPT🤖")
    api_key = st.text_input("Anthropic API Key", type="password")
    st.write("[Get Anthropic API key](https://console.anthropic.com/account/keys)")
    if st.button("Confirm"):
        if api_key != "" or api_key is not None:
            st.session_state.logged_in = True
            os.environ["ANTHROPIC_API_KEY"] = api_key
            st.rerun()
        else:
            st.error("Invalid API Key")
            
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        api_screen()
    else:
        chat_screen()
        
if __name__ == "__main__":
    main()
            