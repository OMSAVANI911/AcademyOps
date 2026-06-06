import re

INTENT_MAPPING = {
    "fees": {
        "keywords": ["cost", "fee", "price", "pay", "tuition", "expensive", "money", "how much"],
        "suggested_stage": "Contacted",
        "reply": "Our program fees vary by track. Would you like us to send a detailed pricing brochure?"
    },
    "timing": {
        "keywords": ["when", "start", "time", "duration", "schedule", "long", "cohort", "hours"],
        "suggested_stage": "Contacted",
        "reply": "Our next cohort starts in two weeks, and classes are held in the evenings. Shall I schedule a quick call?"
    },
    "eligibility": {
        "keywords": ["qualify", "eligible", "requirements", "degree", "background", "need to know", "experience"],
        "suggested_stage": "Qualified",
        "reply": "Our programs are designed for beginners, though basic computer skills are required. Would you like to book a demo call to see if it's a fit?"
    },
    "not-interested": {
        "keywords": ["stop", "unsubscribe", "not interested", "no thanks", "never mind", "cancel"],
        "suggested_stage": "Lost",
        "reply": "Thank you for your time. We have removed you from our active list. Reach out if you ever change your mind!"
    }
}

FALLBACK_INTENT = {
    "intent": "other",
    "suggested_stage": "Contacted",
    "reply": "Thanks for reaching out! One of our counselors will review your message and get back to you shortly."
}

def classify_message(message: str) -> dict:
    """Classifies an inbound message using rule-based keyword matching."""
    msg_lower = message.lower()
    
    for intent, data in INTENT_MAPPING.items():
        for keyword in data["keywords"]:
            # Using regex word boundary to avoid partial matches
            if re.search(r'\b' + re.escape(keyword) + r'\b', msg_lower):
                return {
                    "intent": intent,
                    "suggested_stage": data["suggested_stage"],
                    "reply": data["reply"]
                }
                
    return FALLBACK_INTENT

# Labelled test set for accuracy evaluation
TEST_SET = [
    {"message": "How much does the data science bootcamp cost?", "expected": "fees"},
    {"message": "When does the next web dev batch start?", "expected": "timing"},
    {"message": "Do I need a computer science degree to join?", "expected": "eligibility"},
    {"message": "Please stop emailing me, I am no longer looking.", "expected": "not-interested"},
    {"message": "Can I get some more info?", "expected": "other"},
    {"message": "What is the tuition fee?", "expected": "fees"},
    {"message": "How many hours a week will this take?", "expected": "timing"}
]

def evaluate_accuracy():
    """Runs the classifier against the labelled test set to report accuracy."""
    correct = 0
    total = len(TEST_SET)
    print("\n--- Running WP-08 Classifier Evaluation ---")
    for test_case in TEST_SET:
        result = classify_message(test_case["message"])
        predicted = result["intent"]
        expected = test_case["expected"]
        
        status = "✅" if predicted == expected else "❌"
        print(f"{status} Msg: '{test_case['message']}'\n   Expected: {expected} | Got: {predicted}\n")
        if predicted == expected:
            correct += 1
        
    accuracy = (correct / total) * 100
    print(f"-------------------------------------------")
    print(f"Accuracy: {accuracy:.2f}% ({correct}/{total})\n")

if __name__ == "__main__":
    evaluate_accuracy()