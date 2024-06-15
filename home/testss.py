from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

def is_image_valid_mri(validator_model,path,threshold):
    img = cv2.imread(path)
    resize = tf.image.resize(img, (32,32))
    model_prediction = validator_model.predict(np.expand_dims(resize/255,0))
    if model_prediction[0][0] > threshold:
        return "invalid"
    else:
        return "valid"
    
# def check_for_dementia(model,path):
#     img = cv2.imread(path)
#     resize = tf.image.resize(img, (256,256))
#     model_prediction = model.predict(np.expand_dims(resize/255,0))
#     predicted_class = model_prediction.argmax(axis=1)[0]
   
#     if predicted_class == 0:
#         return "0.0: Cognitively normal"
#     elif predicted_class == 1:
#         return "0.5: Questionable"
#     elif predicted_class == 2:
#         return "1.0: Mildly Demented"
#     else:
#         return "2: Moderatly or Severely demented"

# alzheimer_model = load_model(BASE_DIR / "AI model/CNN_images_only.h5")
validator_model = load_model(BASE_DIR / "AI model/images_validator3.h5")

# full_path = BASE_DIR / "media/images/car.jpg"
full_path = os.path.join(BASE_DIR,"media/images/car.jpg")
# full_path = "C:/Faheem/faheem learns a lot/django/DementiaApp/media/images/car.jpg"
print(full_path)
is_valid = is_image_valid_mri(validator_model,full_path,0.1)

print(is_valid)