from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Memuat model terbaik dari Tugas 3 secara spesifik
model = load_model("model/model_1_klasifikasi.h5")

# Daftar kelas dataset Space Image (sesuai urutan training)
CLASS_NAMES = [
    "constellation", 
    "cosmos space", 
    "galaxies", 
    "nebula", 
    "planets", 
    "stars"
]

# Ukuran disesuaikan menjadi 150x150 sesuai dengan layer input model Tugas 3
def preprocess(img: Image.Image, size=(150, 150)):
    img = img.resize(size)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    x = preprocess(image)
    preds = model.predict(x)
    
    predicted_index = int(np.argmax(preds))
    confidence = float(np.max(preds))
    
    # Mengembalikan label asli dari list CLASS_NAMES
    original_label = CLASS_NAMES[predicted_index]
    
    return {
        "label": original_label,
        "confidence": confidence
    }