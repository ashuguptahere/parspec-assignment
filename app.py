import os
import gdown
import joblib
import numpy as np
import gradio as gr
from tensorflow.keras.models import load_model

MODEL_URL = "https://drive.google.com/uc?id=1PTX_NXhZkoymuni3zpi2lhjpa145lkbm"
MODEL_DIR = os.path.join(os.getcwd(), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "table_classification_model_100.keras")

os.makedirs(MODEL_DIR, exist_ok=True)

# Check if the model file already exists
if not os.path.exists(MODEL_PATH):
    print("Downloading the model from Google Drive")
    gdown.download(MODEL_URL, MODEL_PATH)
else:
    print("Model already exists. Skipping download.")

# Load the model
model = load_model(MODEL_PATH)
if model is None:
    raise ValueError("Model not found")


def load_and_preprocess_image(img):
    img = img.convert("RGB")
    img = img.resize((256, 256))
    img_array = np.array(img)
    img_array = img_array / 255.0
    return img_array


def predict_image_class(img_array):
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    class_probabilities = predictions[0]
    return predicted_class, class_probabilities


def classify_image(image):
    img_array = load_and_preprocess_image(image)
    predicted_class, class_probabilities = predict_image_class(img_array)

    # Mapping of indices to labels
    labels = joblib.load("models/labels.pkl")

    # Convert indices to labels
    mapped_data = dict(zip(labels, class_probabilities))

    # Use the predicted class index to get the label
    class_ = labels[predicted_class] if predicted_class < len(labels) else "Unknown"

    return class_, mapped_data


# Create Gradio interface
demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="pil"),
    outputs=[gr.Textbox(label="Predicted Label"), gr.JSON()],
    title="Image Classification",
    description="Upload an image to classify it into one of the predefined categories: Bordered, Borderless, or Row Bordered.",
    flagging_mode="never",
)

# Launch the app
demo.launch()
