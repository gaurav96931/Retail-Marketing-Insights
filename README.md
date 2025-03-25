# AI-Driven Retail Customer Buying Pattern Predictor

---
## Team Cerulean

## Project Overview

This project is developed for the Microsoft Azure Hackathon with the goal of predicting consumer buying behavior and making customer purchase analytics easily accessible for vendors through Generative AI support.

---

## Objectives

- Predict customer buying behavior based on past purchasing and online browsing patterns.
- Provide insightful analytics for vendors using Azure AI Services.
- Ensure data privacy and security while handling sensitive customer information.
- Offer multilingual support for a global customer base.
- Deploy a web-based interface for real-time insights.

---

## Workflow

This project analyzes retail activity-based data to extract insights and predict customer buying patterns. The pipeline follows a structured approach:

1. *Data Collection* – Gathers and processes historical transaction data.
2. *Machine Learning Model* – Uses ML techniques to detect patterns and forecast future purchases.
3. *Graphical Analysis* – Visualizes trends, seasonality, and insights using interactive charts.
4. *LLM-Enhanced Predictions* – Utilizes Large Language Models (LLMs) to improve prediction accuracy by incorporating contextual understanding.
5. *Multilingual Translation & Privacy Filtering* – Supports multiple languages and ensures the protection of sensitive information.

This solution helps retailers optimize inventory, personalize marketing, and improve customer engagement through AI-driven insights and LLM-enhanced intelligence.

---

## Technology Stack

### Backend

- Flask (Python) – Handles API requests, integrates ML models, and serves frontend data using RESTful APIs.
- Azure SDK for Python
- OpenAI API for Azure
- Python 3.x

### Frontend

- Bootstrap, HTML, CSS – Provides an interactive dashboard for vendors.

### Machine Learning and Data Analysis

- SciKit-Learn – Implements the Random Forest model for customer behavior prediction.
- NumPy, Pandas – Used for data manipulation and preprocessing.
- Matplotlib, Seaborn – Used for data visualization and graphical analysis.
- JSON – Stores and exchanges structured data.

### Development Environment

- VS Code – Used for backend and frontend development.
- Jupyter Notebook – Used for data analysis, model training, and exploratory data analysis (EDA).

---

## Azure Services Used

### Azure OpenAI

Azure OpenAI API is used to generate AI-driven insights by analyzing:

- Machine learning model predictions on customer buying behavior.
- Past purchase patterns to detect trends and correlations.
- Contextual analysis of retail data to enhance decision-making.

### Azure Content Safety

This service filters out sensitive or offensive content from data and reports. It ensures:

- Protection of personal data by removing identifiable customer details.
- Content moderation to prevent inappropriate or harmful information in vendor reports.

### Azure Translator

Azure Translator enables multilingual support, making the analytics dashboard accessible to vendors in different regions. It helps in:

- Translating insights and reports into multiple languages.
- Allowing vendors to interact with AI-generated content in their preferred language.

### Azure Language Services

Azure Language Services are used for text processing and understanding, improving the AI’s ability to analyze and summarize retail insights. It helps in:

- Extracting key insights from customer reviews and feedback.
- Summarizing large datasets into concise, actionable information for vendors.

By integrating these Azure AI services, the system ensures accurate predictions, secure data handling, multilingual accessibility, and improved retail decision-making.

---

## Installation and Setup

### Prerequisites

- Python 3.x
- Azure account with required AI services enabled
- Git installed on your machine

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/gaurav96931/Retail-Marketing-Insights.git
   ```
   
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables for Azure services.
4. Run the Flask API:
   ```sh
   python src/api.py
   ```
5. Open http://localhost:5000 in your browser to access the dashboard.

---

## Repository Structure

```
Retail-Marketing-Insights/
│── static/                      # Static files (CSS, JS, images)
│── templates/                   # HTML templates for frontend
│   ├── dashboard.html
│   ├── index.html
│── venv/                        # Virtual environment
│── .gitignore                   # Git ignore file
│── app.py                        # Flask application
│── customer_history.json        # Sample customer history data
│── dff.py                        # Data processing script
│── LICENSE                      # Project license
│── README.md                    # Project documentation
│── requirements.txt             # Required dependencies
│── test.csv                      # Sample dataset
│── trained_model.pkl             # Trained ML model
```

---


## Contributors

- Harshit Tomar 2201AI15 (https://github.com/owl-Dr)
- Divyam Gupta 2201AI48 (https://github.com/DivyamGupta12)
- Gaurav Kumar 2201CS25 (https://github.com/gaurav96931)
- Harsh Dahiya 2201CS30 (https://github.com/dark-369)
- Ankit Singh  2201AI47 (https://github.com/Ankit-git463)

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/gaurav96931/Retail-Marketing-Insights/blob/main/LICENSE) file for details.

---