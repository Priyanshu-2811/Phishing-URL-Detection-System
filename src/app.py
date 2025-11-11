from flask import Flask, request, render_template
import numpy as np
import pickle
import os
from feature import FeatureExtraction

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'model', 'model.pkl')
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model not found! Please run the training notebook first.")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('index.html', 
                             prediction_text="Error: Model not loaded. Please train the model first.")
    
    try:
        # Get URL from form
        url = request.form['url']
        print(f"Analyzing URL: {url}")
        
        # Extract features using our FeatureExtraction class
        obj = FeatureExtraction(url)
        features = np.array(obj.getFeaturesList()).reshape(1, -1)
        print(f"Features shape: {features.shape}")
        print(f"First 5 features: {features[0][:5]}")
        
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        print(f"Prediction: {prediction}, Probabilities: {prediction_proba}")
        
        # Determine result (model returns 1 for phishing, -1 for legitimate)
        # prediction_proba[0] = probability of class -1 (legitimate)
        # prediction_proba[1] = probability of class 1 (phishing)
        if prediction == 1:
            result = "PHISHING"
            confidence = prediction_proba[1] * 100
            message = f"⚠️ UNSAFE - {confidence:.1f}% phishing risk"
            alert_class = "danger"
        elif prediction == -1:
            result = "LEGITIMATE"
            confidence = prediction_proba[0] * 100
            message = f"✅ SAFE - {confidence:.1f}% legitimate"
            alert_class = "safe"
        else:
            result = "UNKNOWN"
            message = f"❓ UNCERTAIN - Unable to classify (prediction: {prediction})"
            alert_class = "warning"
        
        print(f"Final result: {message}")
        return render_template('index.html',
                             prediction_text=message,
                             result=result,
                             alert_class=alert_class,
                             url=url)
    
    except Exception as e:
        print(f"Error analyzing URL: {e}")
        url = request.form.get('url', '')
        return render_template('index.html',
                             prediction_text=f"❌ Error: Could not analyze URL - {str(e)}",
                             alert_class="warning",
                             url=url)

if __name__ == '__main__':
    app.run(debug=True)