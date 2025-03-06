📜 **WizGuide** - AI-powered Text Translation and Speech-to-Text Application</summary>

  **WizGuide** is an advanced web application that uses AI to translate text and provides a voice-to-text service. The app offers a smooth translation experience for text with the option of generating comments, and it also supports speech-to-text translation using **Google Speech API**. The project is deployed using **Docker** on **DigitalOcean**, making it easy to manage and scale.

  ## 🔧 **Technologies Used**

  ### 🖥️ **Backend (Web Application)**:
  - **Django**: The main backend framework for handling HTTP requests, rendering pages, and managing the database. Django is used for user management, text translation, and saving chat history. It also utilizes **Django’s built-in authentication system** for secure user login and registration.
  - **OpenAI GPT-3.5**: The core AI service for text translation and generating comments or explanations for translated text.
  - **PostgreSQL**: The database used for storing user data, chat histories, translations, and other application-related data.
  - **Docker**: Containerization tool used for creating a consistent environment for the application. The entire application is containerized for deployment and scalability.
  - **DigitalOcean**: Cloud hosting platform used for deploying the app. It provides reliable and scalable hosting, ensuring that **WizGuide** remains available and responsive.

  ### 🎙️ **Backend (Speech-to-Text)**:
  - **FastAPI**: A modern and fast web framework used for the voice translation part of the application. FastAPI serves as the backend for handling voice-to-text requests and integrating with the Google Speech API.
  - **Google Speech-to-Text API**: Used to convert voice input into text. Users can speak into the application, and the app will transcribe the speech into the translated text.

  ### 🌐 **Frontend**:
  - **HTML/CSS/JavaScript**: The core frontend technologies for building the user interface.
  - **Bootstrap**: A responsive design framework for easy and fast UI development. It helps in making the application mobile-friendly.
  - **AJAX**: For handling real-time requests without reloading the page, improving the user experience when interacting with the translation features.

  ### 🗣️ **Voice Features**:
  - **Google Speech API**: Converts spoken language into text, enabling the voice-to-text translation functionality in the app.

  ### 🧑‍💻 **Development and Deployment Tools**:
  - **Docker**: Used for creating isolated environments for both the web application and the speech-to-text service. It ensures consistent development environments across different machines and simplifies deployment.
  - **DigitalOcean**: The app is deployed on DigitalOcean's cloud infrastructure. The platform offers scalability, reliability, and ease of use to host the application in production.

  ## 🔑 **Key Features**:
  - **Text Translation**: Translate text between various languages.
  - **Voice-to-Text Translation**: Use Google Speech API to convert speech into text and translate it.
  - **Comment Generation**: Generate explanatory comments about the translation.
  - **Chat History**: Store translations and comments in the user's chat history.
  - **Multi-language Support**: The app supports multiple languages for the interface, translations, and comments.

  ## 🚀 **App Workflow**:
  1. **Text Translation**: Users enter text, select the source and target languages, and get the translated text. Optionally, they can also receive comments explaining the translation.
  2. **Voice Input**: Users can speak into the app, and the speech will be transcribed into text, which will then be translated and displayed.
  3. **Chat History**: Every translation and comment is saved in the user’s chat history for future reference.

  ## 🚀 **Deployment**
  - **Docker**: All components of the app, including the Django app and FastAPI for speech-to-text, are containerized with Docker. This ensures smooth and consistent deployment on any system.
  - **DigitalOcean**: The app is deployed on DigitalOcean, allowing for fast scaling and reliable uptime.

  ## 📂 **Links**:
  - [GitHub Repository](https://github.com/AlexDCI/WizGuide-fn.git)
  - [Test the Application](http://167.71.34.6:8001)
  - [Documentation and Setup Instructions](https://github.com/AlexDCI/WizGuide-fn.git/blob/main/README.md)

  ---

  ### 📚 **Installation and Setup Instructions**
  To run **WizGuide** locally, clone this repository and follow the setup instructions in the documentation. You can also refer to the Docker setup instructions for a seamless development environment.

 ## 🛠 Installation and Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/AlexDCI/WizGuide-fn.git
cd WizGuide-fn
2️⃣ Create a Virtual Environment
bash
python3 -m venv venv
Activate it:

Windows (CMD):
bash

venv\Scripts\activate
Windows (PowerShell):
bash

venv\Scripts\Activate.ps1
MacOS/Linux:
bash

source venv/bin/activate
3️⃣ Install Dependencies
bash

pip install -r requirements.txt
4️⃣ Apply Database Migrations
bash

python manage.py makemigrations
python manage.py migrate
5️⃣ Create a Superuser (Optional)
bash

python manage.py createsuperuser
6️⃣ Run the Development Server
bash

python manage.py runserver
Open: http://127.0.0.1:8000

🐳 Running with Docker
1️⃣ Build the Docker image:
bash

docker build -t wizguide .
2️⃣ Run the container:
bash

docker run -d -p 8000:8000 wizguide
Open: http://127.0.0.1:8000

🚀 Production Deployment (DigitalOcean)
The app is deployed using Docker on DigitalOcean.
Uses PostgreSQL in production.
Requires Gunicorn and NGINX for optimal performance.
Docker Compose is recommended for managing services.
📂 Links
📌 GitHub Repository: https://github.com/AlexDCI/WizGuide-fn.git
🌐 Live App: http://167.71.34.6:8001
🔥 Contributing
Feel free to contribute! Fork the repo, make changes, and submit a pull request.

📝 License
This project is licensed under the MIT License.
```bash
