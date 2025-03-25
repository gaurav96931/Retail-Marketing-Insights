from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import requests
import json
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__)

# Load your trained ML model (update the file name/path as needed)
MODEL_PATH = "trained_model.pkl"
model = joblib.load(MODEL_PATH)

# Azure OpenAI configuration (Replace with your actual details)
AZURE_OPENAI_ENDPOINT = "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

def get_feature_explanation(features, prediction):
    """
    Calls Azure OpenAI GPT-4 to explain which features influenced the prediction.
    """
    prompt = f"The model predicted {prediction} based on the following features: {features}. Explain which features contributed the most and why."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are an AI assistant expert in explaining machine learning predictions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

def generate_visuals(df):
    """
    Generates Plotly visualizations (a bar chart and a pie chart) based on the prediction data.
    """
    # Example: Bar chart for distribution of product categories (if available)
    if "product_category" in df.columns:
        bar_fig = px.bar(df, x="product_category", title="Product Category Distribution")
        bar_html = pio.to_html(bar_fig, full_html=False)
    else:
        bar_html = "<p>No product category data available for bar chart.</p>"
    
    # Example: Pie chart for payment method distribution (if available)
    if "payment_method" in df.columns:
        pie_fig = px.pie(df, names="payment_method", title="Payment Method Distribution")
        pie_html = pio.to_html(pie_fig, full_html=False)
    else:
        pie_html = "<p>No payment method data available for pie chart.</p>"
    
    return bar_html, pie_html

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Accept CSV file from the form upload
        file = request.files["file"]
        df = pd.read_csv(file)
        
        # Make predictions using the loaded model
        predictions = model.predict(df)
        df["Prediction"] = predictions
        
        # For explanation, list the feature names used (you can customize this as needed)
        features_used = list(df.columns)
        
        # Get an explanation from Azure OpenAI about feature contributions
        explanation = get_feature_explanation(features_used, predictions.tolist())
        
        # Generate visualizations
        bar_chart, pie_chart = generate_visuals(df)
        
        # Convert DataFrame to an HTML table for display
        table_html = df.to_html(classes="data", index=False)
        
        return render_template("dashboard.html",
                               table_html=table_html,
                               explanation=explanation,
                               bar_chart=bar_chart,
                               pie_chart=pie_chart)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)