# Alzheimer's Diagnosis App

## Overview

The **Alzheimer's Diagnosis App** is a Flask-based web application that utilizes deep learning models to predict the stage of Alzheimer's disease from brain MRI images. Users can upload MRI scans to receive a diagnosis, including confidence scores and detailed information about the predicted cognitive decline stage. The app also provides history tracking for past uploads.

## Features

- Upload brain MRI images for diagnosis.
- Get real-time predictions on Alzheimer's disease stages.
- Confidence score for the diagnosis.
- Detailed information about each stage, including:
  - Description of the stage.
  - Common symptoms.
  - Care recommendations.
- User authentication and upload history tracking.
- Clean, user-friendly interface with responsive design.

## Demo

![Upload Page](https://github.com/oladokedamilola/alzheimers-diagnosis-app/blob/master/alz3.png?raw=true)
![Diagnosis Results](path-to-your-results-page-image)

## How It Works

1. **Image Upload**: Users can upload brain MRI scans (in supported image formats).
2. **Prediction**: The uploaded image is processed and passed through a pre-trained deep learning model that classifies it into one of several Alzheimer's disease stages.
3. **Results**: The app returns the predicted stage along with a confidence score, a description of the stage, symptoms, and care recommendations.
4. **History**: Users can view previously uploaded images and their respective diagnoses in the history section.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **Machine Learning**: TensorFlow/Keras for Alzheimer's stage classification model
- **Authentication**: Flask-Login for user authentication
- **Image Processing**: OpenCV for image preprocessing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/oladokedamilola/alzheimers-diagnosis-app.git
   ```

2. Navigate to the project directory:
   ```bash
   cd alzheimers-diagnosis-app
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```bash
   flask db upgrade
   ```

6. Run the app:
   ```bash
   flask run
   ```

## Usage

- Sign up and log in to the app.
- Upload MRI scans through the upload page.
- View the diagnosis results with detailed stage information.
- Check your upload history to review past diagnoses.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
