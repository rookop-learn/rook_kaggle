import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

# Mock function to simulate model response
def model(query):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Please response to the user queries"),
            ("user", "Question:{question}"),
            ("assistant", "Answer:")
        ]
    )
    llm = Ollama(model="llama3.2")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain.invoke({"question": query})

# def model(query):
#     return "Hi Bro Give me a Model"  # Placeholder for actual model response

# Streamlit app configuration
st.set_page_config(page_title="Langchain rohan",page_icon="🤖")
st.title('Chat with URL')
# --- Initialize session state ---
if "history" not in st.session_state:
    st.session_state.history = [
        AIMessage(content="Hello! I'm your assistant. How can I help you today?")
    ]

# Sidebar for URL or PDF input
with st.sidebar:
    st.sidebar.header("Chat with URL or PDF")
    url = st.text_input("Enter the URL to chat with", key="url_input")
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_upload")
    if st.button("🧹 Clear"):
        st.session_state.history = [
            AIMessage(content="How can I help now?")
        ] 
        st.rerun()

# Main chat input
query = st.chat_input("Enter your question",)

        
    
# Process the input and generate a response

if query is not None and query != "":
    answer = model(query)     
    st.session_state.history.append(HumanMessage(content=query))
    st.session_state.history.append(AIMessage(content=answer))

for message in st.session_state.history:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

#to run This - python -m streamlit run url-chat.py or streamlit run url-chat.py