# SmartCityConnect 🌆
 
A full-stack Django web application that intelligently connects users with local service providers (plumbers, electricians, etc.) through an AI-powered chatbot interface. Describe your problem, and find the right pro for the job.

![SmartCityConnect Screenshot](static/screenshot.png) <!-- You'll need to add a screenshot -->

## ✨ Features

- **🤖 AI-Powered Service Matching**: Describe your issue in plain language, and our chatbot will match you with the most relevant service providers.
- **👥 Dual User System**: Separate onboarding flows for Customers and Service Providers.
- **📋 Service Management**: Providers can create, edit, and manage their service listings.
- **🔍 Smart Search & Filtering**: Find providers by service, rating, location, and availability.
- **💬 Built-in Messaging System**: Communicate with providers directly through the platform to discuss details.
- **⭐ Review & Rating System**: Build trust through community feedback.

## 🛠️ Tech Stack

- **Backend:** Python, Django, Django REST Framework (if used)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (Development)
- **AI Component:** OpenAI API 
- **Other:** Pillow (for image handling), etc.


**Test Credentials:**
- Customer: `customer@demo.com` / `password123`
- Provider: `provider@demo.com` / `password123`

## 📦 Installation & Local Setup

Follow these steps to run this project locally on your machine.

1.  **Clone the repository**
    ```bash
    git clone https://github.com/amnaijaz2/SmarCityConnect.git
    cd SmarCityConnect
    ```

2.  **Create a virtual environment and activate it**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

7.  **Open your browser** and go to `http://127.0.0.1:8000`

## 🤖 How the AI Chatbot Works

[Explain in 2-3 sentences how you implemented the "AI" functionality. Be honest and specific. For example:]
"The chatbot feature uses the OpenAI API. When a user describes their problem, their query is sent to the API, which categorizes the request (e.g., 'plumbing', 'electrical') and suggests keywords. These keywords are then used to filter the database of service providers."

## 📁 Project Structure

