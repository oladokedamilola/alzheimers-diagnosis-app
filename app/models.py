from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    uploads = db.relationship('UploadHistory', backref='user', lazy=True)  # Linking uploads to user

    def __repr__(self):
        return f'<User {self.username}>'
    
class AlzheimersInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(50), unique=True, nullable=False)
    class_name = db.Column(db.String(50), nullable=False, unique=True)  # Class name for model
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    care_recommendations = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<AlzheimersInfo(stage={self.stage})>"

class UploadHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    predicted_class = db.Column(db.String(100))
    predicted_stage = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    description = db.Column(db.Text)  # Add this field
    symptoms = db.Column(db.Text)  # Add this field
    care_recommendations = db.Column(db.Text)  # Add this field

    def __repr__(self):
        return f"<UploadHistory(user_id={self.user_id}, stage={self.predicted_stage}, timestamp={self.timestamp})>"
