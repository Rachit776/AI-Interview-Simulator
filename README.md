# AI Interview Simulator

An interactive platform that simulates technical interviews using AI, helping developers prepare for real-world interviews across various domains.

## 🌟 Features

- **Multiple Technical Domains**: Practice interviews in:
  - Frontend Development
  - Backend Development
  - DevOps
  - Machine Learning
  - System Design
  - Graphic Design

- **Interactive Interview Experience**:
  - Real-time audio-based responses
  - AI-powered question recommendations
  - Progress tracking and performance analytics
  - Detailed reports and feedback

- **User Authentication**:
  - Google OAuth integration
  - Secure user profiles
  - Progress persistence

## 🛠️ Technology Stack

### Frontend
- React.js with Vite
- React Router for navigation
- Modern UI components and charts (ApexCharts)
- Toast notifications for better UX
- Responsive design with icons and progress indicators

### Backend
- Flask (Python)
- NLTK for natural language processing
- RESTful API architecture
- CORS support for cross-origin requests
- Environment-based configuration

## 📋 Prerequisites

- Node.js (Latest LTS version)
- Python 3.8+
- pip (Python package manager)

## 🚀 Getting Started

### Backend Setup

1. Navigate to the Flask directory:
   ```bash
   cd Flask
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the Flask directory with necessary configurations.

5. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the client/Frontend directory:
   ```bash
   cd client/Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file with required configurations including Google OAuth client ID.

4. Start the development server:
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Backend (.env)
```
PORT = 
MONGOURL =
JWT_SECRET=

CORS_ORIGIN="*"
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASS=
RABBITMQ_URL=
VITE_FLASK_URL=

CLIENT_URL=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
SESSION_SECRET=
```

### Frontend (.env)
```
VITE_GOOGLE_CLIENT_ID=
VITE_FLASK_URL=
```


## 📝 License

This project is open source and available under the MIT License.

## 👥 Authors

- Initial work and maintenance by the AI Interview Simulator team
