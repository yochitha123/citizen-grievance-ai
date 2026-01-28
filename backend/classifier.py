def classify_issue(text):
    text = text.lower()

    if "water" in text:
        return "Water Supply"
    elif "road" in text or "pothole" in text:
        return "Road & Infrastructure"
    elif "electric" in text or "power" in text:
        return "Electricity"
    elif "hospital" in text or "health" in text:
        return "Healthcare"
    elif "garbage" in text or "waste" in text:
        return "Waste Management"
    else:
        return "General Complaint"
