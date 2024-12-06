# load_alzheimers_data.py

from app import db, create_app
from app.models import AlzheimersInfo

# Initialize Flask app context
app = create_app()  # Ensure your create_app function initializes the app correctly

# Data to populate in the AlzheimersInfo table
stages_data = [
    {
        "class_name": "NonDemented",
        "stage": "No Cognitive Impairment",
        "description": "Stage 1 is considered normal aging, where there is no noticeable decline in cognitive function.",
        "symptoms": "No significant symptoms, individual functions normally.",
        "care_recommendations": "No special care is needed at this stage. Encourage regular health check-ups and healthy lifestyle choices."
    },
    {
        "class_name": "VeryMildDemented",
        "stage": "Very Mild Cognitive Decline",
        "description": "Minor memory problems, often indistinguishable from normal aging.",
        "symptoms": "Forgetting familiar words or the location of everyday objects.",
        "care_recommendations": "Minimal assistance needed. Encourage memory exercises and social engagement."
    },
    {
        "class_name": "MildDemented",
        "stage": "Mild Cognitive Decline",
        "description": "Friends and family begin to notice subtle issues with memory and concentration.",
        "symptoms": "Difficulty recalling names, noticeable issues at work, forgetting newly read material.",
        "care_recommendations": "Supportive care for memory exercises and organization. Begin exploring options for support if needed."
    },
    {
        "class_name": "ModerateDemented",
        "stage": "Moderate Cognitive Decline",
        "description": "Clear symptoms, including forgetting recent events and personal history.",
        "symptoms": "Greater difficulty performing complex tasks, decreased knowledge of recent events, mood changes.",
        "care_recommendations": "Assistance with daily tasks, caregiver support. Safety measures should be considered in the home."
    },
]

# Load data within application context
with app.app_context():
    for stage_data in stages_data:
        # Check if the entry already exists to prevent duplicates
        if not AlzheimersInfo.query.filter_by(class_name=stage_data["class_name"]).first():
            entry = AlzheimersInfo(
                class_name=stage_data["class_name"],
                stage=stage_data["stage"],
                description=stage_data["description"],
                symptoms=stage_data["symptoms"],
                care_recommendations=stage_data["care_recommendations"]
            )
            db.session.add(entry)
    
    # Commit all entries
    db.session.commit()
    print("Alzheimer's information data populated successfully.")
