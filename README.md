# LLAMA-VISIONX

LlaMA-ViSIONX is a Streamlit web application that allows users to upload images and receive detailed descriptions and relevant questions generated based on the image uploaded by the Llama-4 Scout model. The app also provides audio descriptions using text-to-speech. Also it has LlaMA-Bot (Chatbot), where a user can have an interactive chat for better understanding of image and its descirption.
<br>
https://llamavisionx.streamlit.app/

## Features

- Upload images (jpg, png, jpeg) for analysis.
- Get detailed descriptions of images using Groq API.
- Listen to audio descriptions generated with gTTS.
- View and ask relevant questions generated based on the image uploaded.
- Interactive chat with LlaMA-Bot powered by Llama-4 Scout for better understanding of image and its description.

## Setup

1. Clone the repository.

2. Provide your Groq API key for configuration. You can do this in one of two ways:

- Create a `config.toml` file in the root directory with the following content:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

- Or create a `.env` file in the root directory with the following content:

```
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key.

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Run the Streamlit app with:

```bash
streamlit run app.py
```

Open the URL provided by Streamlit in your browser to use the app.

## Dependencies

- streamlit
- groq
- Pillow
- gtts
- python-dotenv
- toml

## License

This project is licensed under the [MIT License](./LICENSE).

## Notes

- Ensure your API key is kept secure and not hardcoded in the source code.
- The app loads environment variables from `config.toml` if present, otherwise falls back to `.env` file for configuration.

