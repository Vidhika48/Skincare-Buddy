import streamlit as st
import google.generativeai as genai
import pytesseract
from PIL import Image

# Load API key
with open('apikey.txt') as f:
    GEMINI_API_KEY = f.read().strip()

# Configure generative AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro-latest",
    system_instruction="""You are an AI bot called Skincare Buddy, designed to revolutionize  
    skincare and body care routines. Skincare Buddy is the go-to virtual assistant for 
    understanding the role of any skincare or body care product while also highlighting 
    potential hazards and ensuring your safety. Skincare Buddy provides personalized insights
    into each product you're curious about."""
)

# Configure generative AI for personal recommendation
model1 = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro-latest",
    system_instruction="""You are an AI bot called Skincare Buddy, designed to revolutionize
    skincare and body care routines. When provided with skin type and personal concerns you 
    recommend products tailored specifically for the concern asked."""
)

def chat_with_skincare_buddy(input_text):
    chat = model.start_chat(history=[])
    response = chat.send_message(input_text)
    for message in chat.history:
        st.write(f">> {message.role}: {message.parts[0].text}")

def recommendation_model(input_text):
    chat1 = model1.start_chat(history=[])
    response = chat1.send_message(input_text)
    for message in chat1.history:
        st.write(f">> {message.role}: {message.parts[0].text}")

def process_image_and_chat(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Perform OCR on the image
    text = pytesseract.image_to_string(img)
    # Print the extracted text
    st.write("Extracted text from image:")
    st.write(text)
    # Chat with Skincare Buddy using the extracted text
    chat_with_skincare_buddy(text)

def main():
    st.title("Skincare Buddy")
    st.write("Welcome to Skincare Buddy!")
    option = st.radio("Choose an option:", ("Text Input", "Image Input"))

    if option == "Text Input":
        user_input = st.text_input("Enter your skincare topic:")
        if st.button("Submit"):
            chat_with_skincare_buddy(user_input)
    elif option == "Image Input":
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            if st.button("Analyze Image"):
                process_image_and_chat(uploaded_file)
    else:
        st.write("Invalid option. Please select either 'Text Input' or 'Image Input'.")

    st.subheader("Personal Recommendation")
    user_input_reco = st.text_input("Ask for a recommendation based on your skin type and concerns:")
    if st.button("Get Recommendation"):
        recommendation_model(user_input_reco)

if __name__ == "__main__":
    main()