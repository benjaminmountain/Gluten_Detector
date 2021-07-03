# Run command below before running program
# export GOOGLE_APPLICATION_CREDENTIALS=gluten-detector-0fc76b3378ba.json
import io
import cv2
from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types

glutenIngredients = ['WHEAT', 'BARLEY', 'RYE']

# Instantiates a client
client = vision.ImageAnnotatorClient()
def detect_text(path):
    """Detects text in the file."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = ''

    for text in texts:
        string+=' ' + text.description
    return string

gluten_flag = 0;
j = 0
cap = cv2.VideoCapture(0)

# Take 8 images then exit if no gluten detected
while not gluten_flag and j < 8:
    # Capture frame-by-frame
    ret, frame = cap.read()
    file = 'live.png'
    cv2.imwrite(file,frame)

    # print OCR text
    text = detect_text(file)
    print(detect_text(file))

    for i in range(len(glutenIngredients)):
        if(text.find(glutenIngredients[i]) != -1):
            print("Gluten Detected: {}".format(glutenIngredients[i]))
            gluten_flag = 1
            break;

    #Display the resulting frame
    cv2.imshow('frame',frame)
    j += 1
if not gluten_flag:
    print("No gluten detected")
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
