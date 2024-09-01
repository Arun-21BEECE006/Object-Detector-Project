from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Ensure the static folders exist
if not os.path.exists('static/images'):
    os.makedirs('static/images')

if not os.path.exists('static/detected'):
    os.makedirs('static/detected')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        # Save the uploaded image
        image = request.files['image']
        uploaded_image_path = 'static/images/uploaded_image.jpg'
        image.save(uploaded_image_path)

        # Run the object detection script
        subprocess.run(['python', 'yolo.py', '--image', uploaded_image_path], check=True)

        # Define the output path for the detected image
        detected_image_path = 'static/detected/detected_image.jpg'

        # Move or rename the output file to the 'static/detected' folder
        if os.path.exists(detected_image_path):
            os.rename(detected_image_path, detected_image_path)

        # Return the path to the output image
        return jsonify({'output_image': f'/static/detected/detected_image.jpg'})
    
    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
