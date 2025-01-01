import torch
import torchvision
from torchvision import transforms
from PIL import Image
import streamlit as st

# Load model
@st.cache_resource
def load_model():
    # Ganti dengan cara kamu meload model
    # model = torchvision.models.mnasnet1_3(weights = 'IMAGENET1K_V1')
    # model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 9)

    # local_metadata = {
    #     'version': 2
    # }
    model = torch.load("MnasNet_weights.pth", weights_only=False, map_location=torch.device("cpu"))
    # model._load_from_state_dict(state_dict, strict = True, local_metadata = local_metadata, prefix = '', 
    #                             missing_keys = None, unexpected_keys = None, error_msgs = None)
    model.eval()  # Set model ke mode evaluasi
    return model

# Preprocess image (sesuaikan dengan kebutuhan model kamu)
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Sesuaikan ukuran dengan model
        transforms.ToTensor(),
        transforms.Normalize(mean = [0.7843, 0.5947, 0.7669], std = [0.0956, 0.1156, 0.0743]),
    ])
    return transform(image).unsqueeze(0)  # Tambahkan dimensi batch

# Predict function
def predict_image(image, model):
    input_tensor = preprocess_image(image)
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = output.argmax(dim=1).item()
    return probabilities, predicted_class

# Untuk menjalankan server, gunakan perintah berikut di terminal:
# uvicorn api:app --reload