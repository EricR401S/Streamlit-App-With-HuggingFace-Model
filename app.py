import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from transformers import GPT2TokenizerFast, ViTImageProcessor, VisionEncoderDecoderModel
from gtts import gTTS

# Load a fine-tuned image captioning model and corresponding tokenizer and image processor
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Function to generate caption from image URL
def generate_caption(image_url):
    try:
        image = Image.open(requests.get(image_url, stream=True).raw)
        pixel_values = image_processor(image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text
    except Exception as e:
        return str(e)

# Streamlit app
def main():
    st.title("Image Captioning with Text-to-Speech")

    # Input image URL
    image_url = st.text_input("Enter Image URL:")

    if st.button("Generate Caption"):
        if image_url:
            # Generate caption
            caption = generate_caption(image_url)
            st.write("Caption:")
            st.write(caption)

            # Option to listen to the caption audio
            if st.button("Listen to Caption Audio"):
                try:
                    tts = gTTS(caption, lang='en')
                    audio_file = BytesIO()
                    tts.write_to_fp(audio_file)
                    st.audio(audio_file)
                except Exception as e:
                    st.error(f"Error generating audio: {str(e)}")

        else:
            st.warning("Please enter an image URL.")

if __name__ == "__main__":
    main()