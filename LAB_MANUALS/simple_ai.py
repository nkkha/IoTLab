from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("/Users/nkkha/Documents/IoTLab/LAB_MANUALS/keras_model.h5", compile=False)

# Load the labels
class_names = ["0 DEO KHAU TRANG", "1 KHONG DEO KHAU TRANG", "2 KHONG CO NGUOI"]

# CAMERA can be 0 or 1 based on default camera of your computer
# camera = cv2.VideoCapture("http://172.16.0.205:4747/video")
camera = cv2.VideoCapture(0)

def image_detector():
    # Grab the webcamera's image.
    ret, image = camera.read()
    res, frame = cv2.imencode('.jpg', image)
    data = base64.b64encode(frame)
    print(len(data))

    if len(data) > 102400:
        print("Image is too big!")
    else:
        print("Publish image: ")

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    # cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print(" - Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    return class_name[2:], data

# # Listen to the keyboard for presses.
# keyboard_input = cv2.waitKey(1)

# # 27 is the ASCII for the esc key on your keyboard.
# if keyboard_input == 27:
#     break

# camera.release()
# cv2.destroyAllWindows()
