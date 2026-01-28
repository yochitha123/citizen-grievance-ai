def get_urgency(sentiment):
    if sentiment == "Negative":
        return "High"
    elif sentiment == "Neutral":
        return "Medium"
    else:
        return "Low"

def priority_score(sentiment, urgency):
    score = 0

    if sentiment == "Negative":
        score += 2
    if urgency == "High":
        score += 2
    elif urgency == "Medium":
        score += 1

    return score
