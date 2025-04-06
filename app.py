import re
import streamlit as st
from interview_assistant import InterviewAssistant

# Initialize the InterviewAssistant class
interview_assistant = InterviewAssistant()

# Streamlit app header
st.header("TalentScout Interview Assistant")

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for the initial message
if "inisial_message" not in st.session_state:
    st.session_state.inisial_message = []

# Display the initial message from the assistant
with st.chat_message("assistant"):
    msg_to_candidate = (
        "To assist you better, we kindly request your name, email, and phone number. "
        "Your information will be handled securely and will not be shared with anyone. "
        "We follow all GDPR guidelines to protect your privacy. Do you agree to share this information?"
    )
    st.markdown(msg_to_candidate)
    st.session_state.inisial_message.append({"role": "assistant", "content": msg_to_candidate})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
  
    # Get the assistant's response
    response = interview_assistant.interview_process_by_assistant(
        prompt, [st.session_state.inisial_message, st.session_state.messages]
    )

    # Extract JSON data from the response using regex
    pattern = r'(\{\s*"full_name":.*\})'
    match = re.search(pattern, response, re.DOTALL)

    if match:
        extracted_json = match.group(1)  # Extract the JSON string
        print(extracted_json)  # Print the extracted JSON (for debugging)

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
