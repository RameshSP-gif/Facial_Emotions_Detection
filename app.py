import os
from flask import Flask, render_template, request
from deepface import DeepFace
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    emotion_result = None
    image_path = None
    emotion_scores = None

    if request.method == 'POST':
        if 'image' not in request.files:
            emotion_result = "No file part"
        else:
            file = request.files['image']
            if file.filename == '':
                emotion_result = "No selected file"
            elif file:
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)

                try:
                    result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
                    emotion_scores = result[0]['emotion']
                    emotion_result = result[0]['dominant_emotion']
                    print("Emotion scores:", emotion_scores)
                except Exception as e:
                    emotion_result = f"Error: {str(e)}"

    return render_template('index.html', emotion=emotion_result, emotions=emotion_scores, image=image_path)

if __name__ == '__main__':
    # Use PORT environment variable from Railway, default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
