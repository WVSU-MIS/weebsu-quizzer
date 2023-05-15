import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import openai
import hashlib
import random
import string

openai.api_key = st.secrets["API_key"]

def perform_task(input_topic, input_competencies): 
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
         {"role": "system", "content": "You are examGPT, a professional exam creator tool. \
      Follow the instructions below: 1. Ensure you adhere closely to the given instructions of the user. \
      2. Think in a step by step fashion. 4. Follow exactly the format of the output"},
          {"role": "user", "content": "Create a 10-item multiple choice exam with exactly 4 choices \
      for each question, based on the learning competencies listed below. Vary the \
      difficulty of each item: 60% easy, 30% medium, and 10% difficult. \
      Subject Title: " + input_topic + \
      "Learning Competencies: " + input_competencies + \
      "Ensure that you use different levels of Bloom's Taxonomy exclude highest level. \
      Provide the correct answer at the end of each question. \
      Format the questions, options and answers in a table formatted as rows in a csv file"}
        ]
    )
    
    # output generated response
    answer = response['choices'][0]['message']['content']
    return answer

# Define the Streamlit app
def app():
    st.title("Weebsu quizGPT")
    st.subheader("A proof of concept of using generative AI for specialized tasks.")
    
    st.write("The quiz generated by this tool is for review purposes only.  We limited the output to just 10 items to minimize the storage and computational load.")

    st.write("The tool is experimental so the output may not be consistent.")
    
    # Create a multiline text field
    topic = "Neural Networks, Deep Learning Tensorflow and Keras"
    input_topic = st.text_input('Input the topic (replace the sample below): ', topic)
    competencies = "1. Understanding of neural network architectures, feedforward and backpropagation principles\
      \n2. Knowledge of activation functions, loss functions, and optimization algorithms\
      \n3. Familiarity with deep learning frameworks, such as TensorFlow, PyTorch, and Keras"
    input_competencies = st.text_area('Input the competencies (replace the sample below):', competencies)   

    # Display the text when the user submits the form
    if st.button('Submit'):
        output = perform_task(input_topic, input_competencies)
    
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        filename = 'quiz-' + random_string + '.csv'

        # save the string to a CSV file
        with open(filename, 'w') as file:
            file.write(output)

        # Generate a download link for the CSV file
        with open(filename, 'rb') as file:
            csv_data = file.read()

        st.download_button(label='Download CSV', data=csv_data, \
                           file_name='output.csv', mime='text/csv')
    
    st.write('\n\n\nDisclaimer: Weebsu may produce inconsistent file format.')
    st.write('\n\n\n© 2023 West Visayas State University - Management Information System Office.')

    text = "*WVSU at the forefront of AI-research in Western Visayas.*"
    st.markdown(text)

# Run the app
if __name__ == "__main__":
    app()
