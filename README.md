# Medical-Diagnosis

A LLM / web-application for medical diagnosis.

## 🧠 Project Overview

This project provides an end-to-end pipeline to perform medical diagnosis using a trained LLM model + a web interface / API backend.

- Model logic lives in the `server/` (or corresponding) folder.
- The web/API layer is exposed via `app.py` / `main.py`.
- Users can upload data / input symptoms / medical records, which the backend uses to generate diagnostic predictions.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/AIAkashMukherjee/Medical-Diagnosis.git
   ```
2. Create and activate a virtual environment:

   ```
   virtualenv my_env

   source my_env/bin/activate
   ```
3. Install dependencies:

   ```
   pip install - requirements.txt
   ```

### 🗂 Repository Structure

Medical-Diagnosis/
├── server/ # Backend + model code
├── uploaded_dir/ # Folder to store user-uploaded files / input data
├── app.py # Entry-point for web or API server
├── main.py # (Optionally) alternative entry point or script
├── requirements.txt # Python dependencies
├── setup.py # Setup / install script (if any)
├── README.md # This file
└── LICENSE # GPL-3.0 license

## How It Works

1. User uploads a medical file or enters symptom text.
2. The text is embedded using  **all-mpnet-base-v2** .
3. Relevant context is retrieved from local store.
4. Prompt is built and sent to  **chatgroq LLaMA-3.1-8B-Instant** .
5. Model returns a structured medical analysis.

## 🧪 Usage

* Upload medical data or input symptoms via the provided UI or API endpoint.
* The backend runs the ML model and returns a diagnosis / prediction.
* (Optional) The results may include additional information such as probabilities, recommended actions, or relevant resources — depending on how the model / app is implemented.

## 🔐 License

This project is licensed under the GPL-3.0 License.
