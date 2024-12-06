from flask import render_template, redirect, url_for, request, current_app, session, flash
from . import main
from .forms import UploadForm
from app.utils import classify_alzheimers_stage
from app.models import AlzheimersInfo, UploadHistory, db  # Assuming you have an UploadHistory model
import os
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

@main.route('/')
def home():
    return render_template('main/home.html')

@main.route("/upload", methods=['GET', 'POST'])
@login_required
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        if form.image.data:
            # Secure and save the uploaded image
            image_file = secure_filename(form.image.data.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            relative_image_path = os.path.join('uploads', image_file).replace("\\", "/")  # Ensure forward slashes
            
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            image_path = os.path.join(upload_folder, image_file)
            form.image.data.save(image_path)

            try:
                # Classify Alzheimer's disease stage
                predicted_class, confidence_score = classify_alzheimers_stage(image_path)
            except Exception as e:
                flash(f"An error occurred during prediction: {e}", "error")
                return redirect(url_for('main.upload_image'))

            # Debugging the predicted stage
            print(f"Predicted Stage: {predicted_class}")

            # Fetch stage info from the database using class_name (updated)
            stage_info = AlzheimersInfo.query.filter_by(class_name=predicted_class).first()
            print(f"Stage Info Retrieved: {stage_info}")  # Debugging line

            # Prepare result data with correct stage name and human-readable stage
            result_data = {
                'predicted_stage': predicted_class,  # This is the model's output
                'stage': stage_info.stage if stage_info else 'Unknown Stage',  # This is the readable stage (e.g., "Very Mild Cognitive Decline")
                'description': stage_info.description if stage_info else 'No description available',
                'symptoms': stage_info.symptoms if stage_info else 'No symptoms available',
                'care_recommendations': stage_info.care_recommendations if stage_info else 'No care recommendations available',
                'image_file': image_file,
                'confidence_score': confidence_score
            }

            # Save the upload history with relevant details
            upload_history = UploadHistory(
                user_id=current_user.id,
                image_path=relative_image_path,
                predicted_class=predicted_class,
                predicted_stage=stage_info.stage,
                confidence_score=confidence_score,
                description=result_data['description'],  # Save description
                symptoms=result_data['symptoms'],  # Save symptoms
                care_recommendations=result_data['care_recommendations']  # Save care recommendations
            )

            # Add the upload history to the session and commit it
            db.session.add(upload_history)
            db.session.commit()

            # Use session for secure redirection
            session['result_data'] = result_data
            return redirect(url_for('main.results'))

    return render_template('main/upload.html', title='Upload Image', form=form)




@main.route("/results")
@login_required
def results():
    result_data = session.get('result_data')
    if not result_data:
        flash("No result data found. Please upload an image first.", category="warning")
        return redirect(url_for('main.upload_image'))
    
    return render_template('main/results.html', **result_data)


@main.route("/history")
@login_required
def history():
    per_page = 10
    page = request.args.get('page', 1, type=int)
    
    # Query for the current user's uploads, ordered by timestamp
    uploads_query = UploadHistory.query.filter_by(user_id=current_user.id).order_by(UploadHistory.timestamp.desc())
    uploads = uploads_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('main/history.html', uploads=uploads)


@main.route("/view_diagnosis/<int:upload_id>")
@login_required
def view_diagnosis(upload_id):
    # Retrieve the upload by ID and check if it belongs to the current user
    upload = UploadHistory.query.get_or_404(upload_id)
    
    if upload.user_id != current_user.id:
        return redirect(url_for('main.home'))

    # Pass the relevant upload data to the template
    return render_template('main/view_diagnosis.html', upload=upload)
