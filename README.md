# Chat Application

A web application that allows users to send interest messages to other users. The recipient can then accept or reject the interest, and if accepted, both users can chat with each other in real time.

## Tech Stack
- **Frontend:** React.js
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT
- **Real-time Communication:** WebSockets

## Core Features

### User Authentication
- Users can register and log in to the platform.

### Sending Interests
- Logged-in users can browse a list of other users and send an interest message.

### Accepting/Rejecting Interests
- Users can view received interest messages and accept or reject them.

### Chat System
- If an interest is accepted, a chat interface is enabled for real-time messaging.

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Node.js (for frontend)
- Python 3 & Django
- PostgreSQL (for database)

### Backend Setup (Django & PostgreSQL)
1. Clone the backend repository:
   ```sh
   git clone https://github.com/Dhinu-2001/PingPong-backend.git
   cd PingPong-backend
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure database settings in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'yourdbname',
           'USER': 'yourdbuser',
           'PASSWORD': 'yourdbpassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
5. Apply migrations and start the server:
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Setup (React.js)
1. Clone the frontend repository:
   ```sh
   git clone https://github.com/Dhinu-2001/PingPong.git
   cd PingPong
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React development server:
   ```sh
   npm run dev
   ```

### Environment Variables
Create a `.env` file in both `backend/` and `frontend/` directories and specify necessary environment variables:

#### Backend `.env`
```
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://yourdbuser:yourdbpassword@localhost:5432/yourdbname
JWT_SECRET=your_jwt_secret
```

#### Frontend `.env`
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.


