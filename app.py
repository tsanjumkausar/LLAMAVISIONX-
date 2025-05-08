import streamlit as st

# Set wide page layout to use full browser width
st.set_page_config(layout="wide")

from groq import Groq
import base64
from PIL import Image
import io
import traceback
from gtts import gTTS
import tempfile
import datetime
import os
import toml
from dotenv import load_dotenv


# Load environment variables from config.toml
try:
    config = toml.load("config.toml")
    for key, value in config.items():
        # Remove quotes if present around the value
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        os.environ[key] = value
except Exception as e:
    st.warning(f"Warning: Could not load config.toml: {e}")

# Load environment variables from .env as fallback
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Validate API key
if not API_KEY:
    st.error("❌ GROQ_API_KEY is missing. Please set it in your config.toml or .env file.")
    st.stop()


def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG") 
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Custom CSS to reduce top padding/margin and push headline higher
st.markdown(
    """
    <style>
    /* Reduce top padding of the main content container */
    .css-18e3th9 {
        padding-top: 0rem;
    }
    /* Reduce margin above the h1 headline */
    h1 {
        margin-top: 0rem;
        padding-top: 0rem;
    }
    /* Add background color to the right column */
    .css-1d391kg > div:nth-child(2) {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Headline centered at the top
st.markdown("<h1 style='text-align: center;'>🖼 LLAMA-VISIONX</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Magic Eyes! Upload an image and hear what it shows.!</p>", unsafe_allow_html=True)

# Create two columns: left for main content, right for chatbot
left_col, right_col = st.columns([2, 1])

with left_col:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        base64_image = encode_image(image)
        client = Groq(api_key=API_KEY)

        if "description" not in st.session_state:
            st.session_state.description = ""

        if "questions" not in st.session_state:
            st.session_state.questions = []
        if "answers" not in st.session_state:
            st.session_state.answers = {}

        with st.spinner("Analyzing image... ⏳"):
            try:
                # Get detailed description of the image if not already generated
                if not st.session_state.description:
                    detailed_prompt = "Provide a detailed description of the following image:"
                    chat_completion = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": detailed_prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                                ],
                            }
                        ],
                    )
                    st.session_state.description = chat_completion.choices[0].message.content

                description = st.session_state.description
                st.success("✅ Analysis Complete!")
                st.write("### 🔍 Description:")
                st.write(description)

                # Generate audio description
                tts = gTTS(text=description, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    temp_filename = tmp_file.name
                try:
                    tts.save(temp_filename)
                    st.audio(temp_filename, format="audio/mp3")
                except Exception as e:
                    st.error(f"⚠ Audio generation failed: {e}")

                # Generate related questions based on the description
                if not st.session_state.questions:
                    question_prompt = f"Based on the following description, generate 5 relevant questions that a user might want to ask:\n\n{description}\n\nQuestions:"
                    question_completion = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": question_prompt,
                            }
                        ],
                    )
                    questions_text = question_completion.choices[0].message.content
                    # Parse questions from the response (assuming numbered list)
                    questions = []
                    for line in questions_text.splitlines():
                        line = line.strip()
                        if line and (line[0].isdigit() or line.startswith("-")):
                            # Remove numbering or bullet
                            question = line.lstrip("0123456789. -").strip()
                            if question:
                                questions.append(question)
                    if not questions:
                        # fallback to some default questions if parsing fails
                        questions = [
                            "What emotions are depicted in this image?",
                            "Can you describe the setting or location?",
                            "What objects or people are prominent?",
                            "What story could this image be telling?",
                            "What colors stand out the most?"
                        ]

                    st.session_state.questions = questions

            except Exception as e:
                error_message = f"⚠ Error: {e}"
                st.error(error_message)
                st.text("Detailed traceback:")
                st.text(traceback.format_exc())

        if st.session_state.questions:
            st.write("### ❓ Related Questions:")
            for question in st.session_state.questions:
                if st.button(question):
                    if question not in st.session_state.answers:
                        with st.spinner("Getting answer... ⏳"):
                            try:
                                answer_completion = client.chat.completions.create(
                                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                                    messages=[
                                        {
                                            "role": "user",
                                            "content": [
                                                {"type": "text", "text": f"Please provide an answer to the question in about 8-10 lines, or split into two paragraphs of roughly equal length: {question}"},
                                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                                            ],
                                        }
                                    ],
                                )
                                answer = answer_completion.choices[0].message.content
                                st.session_state.answers[question] = answer
                            except Exception as e:
                                st.session_state.answers[question] = f"Error getting answer: {e}"
                    st.write(f"Q: {question}")
                    st.write(f"A: {st.session_state.answers.get(question, 'No answer available.')}")

    st.write("Powered by Llama-4 Scout 🚀")

with right_col:
    st.write("---")
    st.write("## 💬 LlaMA-Bot")

    # Welcome message and instructions
    st.write("🧠 Ask. Chat. Explore!")
    st.write("Ask Llama-4 Scout anything—learning just got exciting!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    client = Groq(api_key=API_KEY)

    def get_chat_response(user_input, chat_history):
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Please provide short and concise answers."}
        ]
        for speaker, message in chat_history:
            role = "user" if speaker == "You" else "assistant"
            messages.append({"role": role, "content": message})
        messages.append({"role": "user", "content": user_input})

        try:
            chat_completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def format_message(speaker, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if speaker == "You":
            return f"You [{timestamp}]: {message}"
        else:
            return f"Bot [{timestamp}]: {message}"

    def clear_chat():
        st.session_state.chat_history = []

    if st.button("Clear Chat"):
        clear_chat()

    user_input = st.text_input("You:", key="input")

    if user_input:
        if user_input.strip() == "":
            st.warning("Please enter a valid message.")
        else:
            response = get_chat_response(user_input, st.session_state.chat_history)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

    for speaker, message in st.session_state.chat_history:
        st.markdown(format_message(speaker, message))

