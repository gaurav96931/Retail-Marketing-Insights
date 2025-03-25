from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import requests
import json
import plotly.express as px
import plotly.io as pio
import os
import markdown
import re

app = Flask(__name__)

table_html=None
explanation=None
bar_chart=None,
pie_chart=None,
languages=None
explanation=None

# Load your trained ML model (update the file name/path as needed)
MODEL_PATH = "trained_model.pkl"
model = joblib.load(MODEL_PATH)

# Azure OpenAI configuration (Replace with your actual details)
AZURE_OPENAI_ENDPOINT = "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
AZURE_AI_SERVICES_END_POINT = "https://ai-aihackthonhub282549186415.cognitiveservices.azure.com/"
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"
TRANSLATE_ENDPOINT = "https://ai-aihackthonhub282549186415.cognitiveservices.azure.com/translator/text/v3.0/translate"

# Load customer purchase history JSON
with open("customer_history.json", "r") as f:
    customer_history = json.load(f)

# Expanded language list with Indian languages
LANGUAGES = {
    "French": "fr",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur"
}

HEADERS = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Region": "eastus"
}

def translate_text(text, target_lang):
    """Translate text using Azure Translator API."""
    params = {
        "api-version": "3.0",
        "from": "en",
        "to": [target_lang]
    }
    data = [{"text": text}]
    response = requests.post(TRANSLATE_ENDPOINT, headers=HEADERS, params=params, json=data)
    
    if response.status_code == 200:
        return response.json()[0]['translations'][0]['text']
    else:
        return f"Error: {response.status_code} {response.text}"


# Product category mapping
product_categories = {
    1: "Groceries & Essentials",
    2: "Beverages",
    3: "Personal Care & Hygiene",
    4: "Home & Kitchen Items",
    5: "Electronics & Accessories",
    6: "Clothing & Apparel",
    7: "Toys & Stationery"
}

def get_feature_explanation(features, prediction, customer_id):
    """
    Calls Azure OpenAI GPT-4 to explain which features influenced the prediction.
    Includes past purchase history in the prompt.
    """
    # Get past purchase categories for the customer
    past_purchases = customer_history.get(str(customer_id), [])
    past_categories = [product_categories.get(cat, "Unknown") for cat in past_purchases]

    # Construct prompt
    prompt = (
        f"The model predicted the following probabilities for customer {customer_id}: {prediction}. "
        f"The customer has previously purchased items from these categories: {past_categories}. "
        f"Consider past purchases and trends and based on the past historical data, analyze their buying pattern and the probabilities of the output. suggest what they might purchase and what category are they likely to buy."
        f"Make sure to format the output on these points: General overview, past purchases, model predictions and conclusions. Give it short and to the point."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are an AI assistant expert in explaining machine learning predictions. You will go through the data given to you and give simple results instead of in depth explanation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 600
    }
    
    response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

def generate_visuals(df):
    """
    Generates Plotly visualizations (a bar chart and a pie chart) for the given DataFrame.
    """
    if df.empty:
        return "<p>No data available for visualization.</p>", "<p>No data available for visualization.</p>"

    # Bar Chart: Showing the sum of values for each column
    bar_fig = px.bar(df.sum().reset_index(), x="index", y=0, title="Feature Value Distribution")
    bar_html = pio.to_html(bar_fig, full_html=False)

    # Pie Chart: Showing percentage contribution of each column's sum
    pie_fig = px.pie(df.sum().reset_index(), names="index", values=0, title="Feature Contribution Distribution")
    pie_html = pio.to_html(pie_fig, full_html=False)

    return bar_html, pie_html

def redact_pii(text):
    url = f"{AZURE_AI_SERVICES_END_POINT}/text/analytics/v3.1/entities/recognition/pii"
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/json"
    }
    # The API expects a 'documents' array
    documents = {
        "documents": [
            {"id": "1", "language": "en", "text": text}
        ]
    }

    response = requests.post(url, headers=headers, json=documents)
    response.raise_for_status()  # Raise an error for bad status codes

    results = response.json()
    redacted_text = text

    # Parse the response and replace PII text with a placeholder
    if "documents" in results and results["documents"]:
        for entity in results["documents"][0].get("entities", []):
            redacted_text = redacted_text.replace(entity["text"], "**xyz")

    return redacted_text

def convert_to_markdown(text):
    """
    Convert OpenAI API response (with *, #, etc.) into proper Markdown-formatted HTML.
    """
    # Ensure proper line breaks for Markdown processing
    text = text.replace("\n", "  \n")
    
    # Convert Markdown to HTML
    html_output = markdown.markdown(text)

    return html_output


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def transalte():
    global table_html
    global explanation
    global bar_chart
    global pie_chart
    global languages
    global explanation
    translation = ""
    text = explanation  # Preserve text input
    selected_lang = request.form.get("language", "")  # Preserve selected language
    print("k", text, selected_lang)
    if request.method == "POST" and "translate" in request.form:
        if text and selected_lang:
            translation = translate_text(text, selected_lang)
            print(translation)


    return render_template("dashboard.html", languages=LANGUAGES, translation=translation, explanation=text, selected_lang=selected_lang, bar_chart=bar_chart, pie_chart=pie_chart, table_html=table_html)
    

@app.route("/predict", methods=["POST"])
def predict():
    global table_html
    global explanation
    global bar_chart
    global pie_chart
    global languages
    global explanation
    try:
        # Accept CSV file from the form upload
        file = request.files["file"]
        df = pd.read_csv(file)
        # assuming we are processing one customer at a time
        customer_id = df['customer_id'][0]
        # reomve customer_id column
        df = df.iloc[:, 1:]
        print(df.head())

        # print(type(df), df.shape)
        
        # Make predictions using the loaded model
        predictions = model.predict_proba(df)
        
        probabilities = pd.DataFrame({  # Replace with actual custno if available
                   'Groceries & Essentials': [p[1] for p in predictions[0]],  # Access probabilities for class 1
                   'Personal Care & Hygiene': [p[1] for p in predictions[1]],  # Access probabilities for class 2
                   'Home & Kitchen Items': [p[1] for p in predictions[2]],  # Access probabilities for class 3
                   'Electronics & Accessories': [p[1] for p in predictions[3]],  # Access probabilities for class 4
                   'Clothing & Apparel': [p[1] for p in predictions[4]],  # Access probabilities for class 5
                   'Toys & Stationery': [p[1] for p in predictions[5]]})  # Access probabilities for class 6

        # For explanation, list the feature names used (you can customize this as needed)
        features_used = list(df.columns)
        
        # # # Get an explanation from Azure OpenAI about feature contributions
        explanation = get_feature_explanation(features_used, probabilities, customer_id)
        print(explanation)
        explanation = convert_to_markdown(explanation)
        # explanation = redact_pii(explanation)

        # # # Generate visualizations
        bar_chart, pie_chart = generate_visuals(probabilities)
        
        # # # Convert DataFrame to an HTML table for display
        table_html = probabilities.to_html(classes="data", index=False)
        
        return render_template("dashboard.html",
                               table_html=table_html,
                               explanation=explanation,
                               bar_chart=bar_chart,
                               pie_chart=pie_chart,
                               languages=LANGUAGES)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)