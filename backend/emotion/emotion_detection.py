import cv2
from deepface import DeepFace

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        break

    result = DeepFace.analyze(
        frame,
        actions=['emotion'],
        enforce_detection=False
    )

    emotion = result[0]['dominant_emotion']

    # Angry Alert
    if emotion == 'angry':

        alert_text = 'WARNING: Angry Emotion Detected'
        color = (0, 0, 255)

    else:

        alert_text = f'Emotion: {emotion}'
        color = (0, 255, 0)

    cv2.putText(
        frame,
        alert_text,
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow('AI Sentinel Emotion Detection', frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()