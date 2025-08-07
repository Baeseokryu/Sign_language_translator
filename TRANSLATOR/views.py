# views.py

import cv2
import numpy as np
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from PIL import Image
from io import BytesIO
import base64
import json

# Load model and correct label list (35 classes: A-Z and 0-9 excluding duplicates)
model = load_model("C:/Users/Dell/priya/SLT/SLT/sign_model.h5")
labels = ['1','2','3','4','5','6','7','8','9',
          'A','B','C','D','E','F','G','H','I',
          'J','K','L','M','N','O','P','Q','R',
          'S','T','U','V','W','X','Y','Z','0']

# Homepage view
def home(request):
    return render(request, 'home.html')

# Streaming webcam generator
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Preprocess
        img = cv2.resize(frame, (64, 64))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        # Prediction
        prediction = model.predict(img)
        pred_index = np.argmax(prediction)
        label = labels[pred_index] if pred_index < len(labels) else "Unknown"

        # Display prediction
        cv2.putText(frame, f'Prediction: {label}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Webcam streaming view
def webcam_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

# Live webcam prediction page
def live_prediction(request):
    return render(request, 'live.html')

# Image-based prediction page (not streaming)
def predict_gesture(request):
    return render(request, 'predict.html', {'result': 'Waiting for capture...'})

# Image upload API to predict from base64 image
@csrf_exempt
def predict_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            img_data = data['image'].split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(img_data))).convert('RGB')
            image = image.resize((64, 64))

            img_array = np.array(image).astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)
            pred_index = np.argmax(prediction)
            label = labels[pred_index] if pred_index < len(labels) else "Unknown"

            return JsonResponse({'prediction': label})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
