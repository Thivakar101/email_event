from flask import Flask, render_template, request
import pandas as pd
from event_extraction import extract_event
from reminder import schedule_reminder

app = Flask(__name__)


dataset_path = "dataset.xlsx"
df = pd.read_excel(dataset_path)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    email_text = ""

    if request.method == "POST":
        email_text = request.form["email_text"].strip()  # Ensure clean input
        
        if not email_text:
            message = "Please provide email content."
        else:

            event_name, venue, date, time = extract_event(email_text, df)
            
            if event_name == "Unknown Event":
                message = "Could not extract event details. Please check the email content."
            else:

                schedule_reminder(event_name, date, time, venue)
                message = f"Reminder set for '{event_name}' on {date} at {time} in {venue}."

    return render_template("index.html", message=message, email_text=email_text)  # Pass email_text

if __name__ == "__main__":
    app.run(debug=True)
