import numpy as np
import pandas as pd
from flask import Flask, render_template, request, url_for
import pickle
import logging
import os

# Configure Flask app with proper static folder
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_path='/static')
app.logger.setLevel(logging.INFO)

# Load the trained machine learning model
try:
    model = pickle.load(open('HDI.pkl', 'rb'))
except FileNotFoundError:
    app.logger.warning("Model file 'HDI.pkl' not found. Predictions may not work correctly.")

@app.route('/')
@app.route('/Home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/Prediction', methods=['POST', 'GET'])
def prediction():
    return render_template('indexnew.html')

def validate_input(country, life_exp, schooling, gni, internet_users):
    """Validate input ranges for better accuracy"""
    errors = []
    
    try:
        life_exp = float(life_exp)
        if not (50 <= life_exp <= 89):
            errors.append("Life expectancy must be between 50-89 years")
    except:
        errors.append("Life expectancy must be a valid number")
    
    try:
        schooling = float(schooling)
        if not (1 <= schooling <= 15):
            errors.append("Mean years of schooling must be between 1-15")
    except:
        errors.append("Mean years of schooling must be a valid number")
    
    try:
        gni = float(gni)
        if not (400 <= gni <= 140000):
            errors.append("GNI per capita must be between 400-140,000")
    except:
        errors.append("GNI per capita must be a valid number")
    
    try:
        internet_users = float(internet_users)
        if not (0 <= internet_users <= 100):
            errors.append("Internet users percentage must be between 0-100")
    except:
        errors.append("Internet users must be a valid number")
    
    return errors

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from form submission
        country = request.form.get('Country', '0')
        life_expectancy = request.form.get('Life expectancy', '')
        mean_schooling = request.form.get('Mean years of schooling', '')
        gni_per_capita = request.form.get('Gross national income', '')
        internet_users = request.form.get('Internet users', '0')
        
        # Validate inputs
        validation_errors = validate_input(country, life_expectancy, mean_schooling, gni_per_capita, internet_users)
        if validation_errors:
            error_msg = "Input Errors:<br>• " + "<br>• ".join(validation_errors)
            return render_template('indexnew.html', showcase=error_msg)
        
        # Convert to float
        life_expectancy = float(life_expectancy)
        mean_schooling = float(mean_schooling)
        gni_per_capita = float(gni_per_capita)
        
        # Create feature array for model prediction (using first 4 features as expected)
        features_value = [[float(country), life_expectancy, mean_schooling, gni_per_capita]]
        
        # Structure data into dataframe format matching model columns
        features_name = ['Country', 'Life expectancy at birth', 'Mean years of schooling', 'Gross national income (GNI) per capita']
        df = pd.DataFrame(features_value, columns=features_name)
        
        # Execute predictive target inference
        output = model.predict(df)
        y_pred = round(float(output[0]), 4)  # Improved precision to 4 decimal places
        
        # Enhanced classification thresholds with better accuracy boundaries
        if y_pred < 0.55:
            result_category = f"<span style='color:#ff6b6b;'>⚠ Low HDI: {y_pred}</span>"
            description = "Low human development - focus on improving education and healthcare"
        elif 0.55 <= y_pred < 0.70:
            result_category = f"<span style='color:#ffd93d;'>⬆ Medium HDI: {y_pred}</span>"
            description = "Medium human development - steady progress in social indicators"
        elif 0.70 <= y_pred < 0.80:
            result_category = f"<span style='color:#6bcf7f;'>✓ High HDI: {y_pred}</span>"
            description = "High human development - strong social infrastructure"
        elif y_pred >= 0.80:
            result_category = f"<span style='color:#38bdf8;'>⭐ Very High HDI: {y_pred}</span>"
            description = "Very high human development - excellent socioeconomic indicators"
        else:
            result_category = f"<span style='color:#ff6b6b;'>Invalid: {y_pred}</span>"
            description = "The predicted value is outside expected range"
        
        final_output = f"{result_category}<br><small>{description}</small>"
        return render_template('resultnew.html', prediction_text=final_output)
        
    except ValueError as e:
        error_msg = f"<span style='color:#ff6b6b;'>Input Error: All fields must contain valid numbers</span>"
        return render_template('indexnew.html', showcase=error_msg)
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        error_msg = f"<span style='color:#ff6b6b;'>System Error: {str(e)}</span>"
        return render_template('indexnew.html', showcase=error_msg)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
