import pandas as pd
import spacy
import re
from fuzzywuzzy import process


nlp = spacy.load("en_core_web_sm")

def extract_event(email_text, dataset):
    """."""
    print("📩 Processing Email:", email_text[:100], "...")  # Debugging output
    

    email_text_lower = email_text.lower()
    

    event_names = dataset["Event"].dropna().astype(str).tolist()
    best_match, score = process.extractOne(email_text_lower, event_names)
    
    if score > 80:  
        row = dataset[dataset["Event"].astype(str) == best_match].iloc[0]
        print("✅ Matched Event from Dataset:", best_match)
        
     
        venue = str(row["Venue"]) if pd.notna(row["Venue"]) else "Unknown Venue"
        date = str(row["Date"]) if pd.notna(row["Date"]) else "Unknown Date"
        raw_time = str(row["Time"]) if pd.notna(row["Time"]) else "Unknown Time"

        # Ensure time format is HH:MM
        time_match = re.match(r"(\d{1,2}):(\d{2})", raw_time)
        formatted_time = f"{int(time_match.group(1)):02}:{time_match.group(2)}" if time_match else "09:00"

        return best_match, venue, date, formatted_time
    
  
    doc = nlp(email_text)
    for ent in doc.ents:
        if ent.label_ in ["EVENT", "ORG"]:
            print("🧠 NLP Extracted Event:", ent.text)
            return ent.text, "Unknown Venue", "Unknown Date", "09:00"  # Default time

    print("⚠️ No event details found.")
    return "Unknown Event", "Unknown Venue", "Unknown Date", "09:00"

