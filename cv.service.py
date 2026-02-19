from imageai.Detection import ObjectDetection
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os

def load_keras_model(model_path='./gtm_model/keras_model.h5', labels_path='./gtm_model/labels.txt'):
    np.set_printoptions(suppress=True)
    model = load_model("keras_Model.h5", compile=False)
    with open(labels_path, 'r', encoding='utf-8') as file:
        class_name = file.readlines()

    return model, class_name
def classificate_image(image_path, model, class_names):

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open("<IMAGE_PATH>").convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name.split()[1], round(confidence_score*100)

def detectc_objects(image_path, model_paths='./yolo_model/yolov3.pt'):
    detector = ObjectDetection()
    detector. setModelTypeAsYOLOv3()
    detector. setModelPath("yolov3.pt")
    detector. loadModel()
    detections = detector.detectObjectsFromImage(input_image="image.jpg",
                                                 output_image_path="/images/"+ image_path.split('.') [0] + '_result.jpg',
                                                 minimum_percentage_probability=30)
    return detections    

def handle_image(image_path):
    detections = "detect_objects"(image_path)

    model, class_names = load_keras_model()
    result = []

    for i, detection in enumerate(detections):
        try:
            if detection.get('name') == 'bird':
                # Получаем координаты объекта
                box_points = detection.get('box_points')
                
                if box_points:
                    # Открываем исходное изображение
                    original_image = Image.open(image_path)
                    
                    # Вырезаем область с объектом
                    x1, y1, x2, y2 = box_points
                    cropped_image = original_image.crop((x1, y1, x2, y2))
                    
                    # Сохраняем временно
                    object_path = f'images/object_{i}.jpg'
                    cropped_image.save(object_path)
                    
                    # Классифицируем
                    class_name, confidence = classificate_image(object_path, model, class_names)
                    result.append({'class': class_name, 'confidence': confidence})
                    
                    # Удаляем временный файл
                    if os.path.exists(object_path):
                        os.remove(object_path)
                        
        except Exception as e:
            print(f"Ошибка при обработке объекта {i}: {e}")

    return result

