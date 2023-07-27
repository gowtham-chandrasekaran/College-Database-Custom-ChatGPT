import streamlit as st
from openai_helper import get_answer

from PIL import Image

st.title("College Q&A ChatBot")
st.write("This application uses openAI to retrieve data from a college database. It can also answer any other common questions that you generally ask ChatGPT.")
fees_image = Image.open('/Users/gowthamc/Desktop/openAI project/chatbot_openAI/images/fees.png')
marks_image = Image.open('/Users/gowthamc/Desktop/openAI project/chatbot_openAI/images/marks.png')

# Resize the "marks" image to the desired dimensions (e.g., 300x300)
desired_size = (100, 100)
marks_image_resized = marks_image.resize(desired_size)
# Create two columns layout
col1, col2 = st.columns(2)

# Display images in the columns
with col1:
    st.image(fees_image, caption='Fees data')

with col2:
    st.image(marks_image, caption='Marks data')

st.write("For example you can ask: What is Elon Musk's GPA in the third semester?")
st.write("You can also ask aggregate operation questions like: What was the average marks in semester 2?")
question = st.text_input("Question:")

if question:
    answer = get_answer(question)
    st.text("Answer:")
    st.write(answer)
