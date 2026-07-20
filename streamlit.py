import streamlit as st
from Langraphstreamlit import chatbot
from langchain_core.messages import HumanMessage
import uuid

##### Utilitu function####
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread_id(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread_id(thread_id):
    if thread_id not in st.session_state['chats_thread']:
        st.session_state['chats_thread'].append(thread_id)


def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id': thread_id}}).values['messages']



# Lightweight cached display name helper. Keeps original code intact and
# provides a quick summary for sidebar labels without forcing a network call.
def get_display_name(thread_id):
    key = str(thread_id)
    if 'thread_names' not in st.session_state:
        st.session_state['thread_names'] = {}
    # return cached name if present
    if key in st.session_state['thread_names'] and st.session_state['thread_names'][key] != key:
        return st.session_state['thread_names'][key]

    # prefer the first user/human message as the thread title
    try:
        messages = load_conversation(thread_id)
        first_human = None
        for m in messages:
            if isinstance(m, HumanMessage):
                first_human = getattr(m, 'content', str(m)).strip()
                if first_human:
                    break

        if first_human:
            # take the first line and truncate to keep it short
            title = first_human.split('\n', 1)[0][:60]
        else:
            # fallback: use first message content or the uuid string
            if messages:
                title = getattr(messages[0], 'content', str(messages[0]))[:60]
            else:
                title = key
    except Exception:
        title = key

    st.session_state['thread_names'][key] = title
    return title

#sesssion state->dict
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chats_thread' not in st.session_state:
    st.session_state['chats_thread']=[]

add_thread_id(st.session_state['thread_id'])

CONFIG={'configurable':{'thread_id': st.session_state['thread_id']}}


# message_history=[]


##### Sidebar########
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chats_thread'][::-1]:
    display_label = get_display_name(thread_id)
    if st.sidebar.button(display_label):
        st.session_state['thread_id']=thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]

        for msg in messages:    
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':msg.content})

        st.session_state['message_history']=temp_messages



#loading the conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input=st.chat_input('Type Here:')

if user_input:

    #first add the message to message history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    
    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages')
        )

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})