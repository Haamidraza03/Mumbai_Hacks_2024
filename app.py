import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Set up Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    email_text = ""
    email_topic = ""
    product_description = ""
    
    if request.method == "POST":
        # Retrieve user input
        email_topic = request.form.get("email_topic", "")
        product_description = request.form.get("product_description", "")
        
        # Generate email text
        email_prompt = f"Write a professional email for an ad campaign on the topic: '{email_topic}', focusing on the product description: '{product_description}'."
        email_response = model.generate_content(email_prompt)
        
        # Remove unwanted characters like * and format email text with subject and body style
        email_text = email_response.text.replace("*", "")

    return render_template("index.html", email_text=email_text, email_topic=email_topic, product_description=product_description)

if __name__ == "__main__":
    app.run(debug=True)
