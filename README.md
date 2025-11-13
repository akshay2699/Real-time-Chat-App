📌 Real-Time Chat Application (Full Stack Assignment)

This project is a real-time private chat system built using:

Django + Django REST Framework

Django Channels + WebSockets

Redis (Docker)

React + Vite

TailwindCSS

The app supports:

✔ Real-time messaging
✔ WebSocket updates (send/receive instantly)
✔ Read receipts (✔ / ✔✔ blue)
✔ Typing indicator
✔ Unread message count
✔ Last message preview
✔ Multi-user simulation (switch active user)
✔ Full chat history
✔ Private 1-to-1 rooms

🚀 1. Setup Instructions
⚙ Backend Setup (Django + Channels)
1. Create Virtual Environment
cd backend
python -m venv venv

2. Activate Venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Start Redis (via Docker)
docker run -d --name redis7 -p 6379:6379 redis:7


If Redis already running:

netstat -ano | findstr 6379

5. Run Backend Server (Daphne)
venv\Scripts\python.exe -m daphne -p 8000 chat_backend.asgi:application


Backend runs at:

👉 http://127.0.0.1:8000/

💻 2. Frontend Setup (React + Vite)
cd frontend
npm install
npm run dev


Frontend runs at:

👉 http://localhost:5173/

🔗 3. Project Structure
chat-app/
│
├── backend/
│   ├── chat_backend/          # Django settings + ASGI + URLs
│   ├── chat/                  # WebSocket consumer + models + APIs
│   ├── requirements.txt
│   └── venv/ (ignored)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── node_modules/ (ignored)
│
└── README.md

🧠 4. Features Implemented
Real-Time Messaging

Powered by Django Channels + WebSockets

Zero refresh needed

Typing Indicators

Per user typing status in real time

Read Receipts

Single tick = sent

Double tick = delivered

Blue double tick = read

Unread Message Count

Chat list shows unread badge for the active user

Chat Room List

Shows rooms

Last message

Timestamp

Unread count badge

Multi-user Simulation

Switch between multiple users without login

Message Pagination (20 per page)
Robust Backend

DRF for API

Channels for WebSockets

Redis for WS layers

Clean serializers & views

🛠 5. API Endpoints
List Users
GET /api/users/

List Rooms for Active User
GET /api/rooms/?active_user=<id>

Create/Get 1-to-1 Room
POST /api/rooms/create/
{
  "user_id": <other_user>,
  "active_user_id": <me>
}

Get Messages
GET /api/rooms/<id>/messages/

🔌 6. WebSocket Wiring
ws://127.0.0.1:8000/ws/chat/<room_id>/


Events:

Type	Description
message	New message
typing	User typing
read	Message marked read
