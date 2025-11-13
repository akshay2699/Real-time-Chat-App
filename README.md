# 📌 Real-Time Chat Application (Full Stack Assignment)

A fully-featured **real-time private chat system** built using:

* **Django + Django REST Framework (DRF)**
* **Django Channels (WebSockets)**
* **Redis (via Docker)**
* **React + Vite**
* **TailwindCSS**

### ✔ Features Included

* ⚡ Instant real-time messaging
* 💬 Typing indicators
* ✔✔ Read receipts (sent, delivered, read)
* 🔢 Unread message count
* 📨 Last message preview
* 🙋‍♂️ Multi-user simulation (no login needed)
* 🕒 Chat history with pagination
* 🔐 Private 1-to-1 chat rooms
* ♻ Live room refresh using WebSockets
* 🔄 Auto reconnect for WebSocket stability


# 🚀 1. **Backend Setup** (Django + Channels)

### **1. Create Virtual Environment**


cd backend
python -m venv venv

<<<<<<< HEAD

### **2. Activate Virtualenv**


venv\Scripts\activate


### **3. Install Dependencies**


pip install -r requirements.txt


### **4. Start Redis (via Docker)**


docker run -d --name redis7 -p 6379:6379 redis:7


Check if Redis is running:


netstat -ano | findstr 6379


### **5. Run Backend Server (Daphne)**


venv\Scripts\python.exe -m daphne -p 8000 chat_backend.asgi:application
=======
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
>>>>>>> 4bbb98e862e8c6a6d008917e2827da6a58931e2d


Backend URL:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**


# 💻 2. **Frontend Setup** (React + Vite)

cd frontend
npm install
npm run dev
<<<<<<< HEAD
=======


Frontend runs at:
>>>>>>> 4bbb98e862e8c6a6d008917e2827da6a58931e2d

Frontend URL:
👉 **[http://localhost:5173/](http://localhost:5173/)**


# 📂 3. **Project Structure**


chat-app/
│
├── backend/
│   ├── chat_backend/       # Django settings + ASGI routing
│   ├── chat/               # Consumers, models, serializers, views
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


# 🧠 4. **Features Implemented**

### 🔥 Real-Time Messaging

Implemented using Django Channels + Redis.
Messages appear instantly for both users without page refresh.

### 💬 Typing Indicators

Real-time "typing…" indicator triggered via WebSocket events.

### ✔✔ Read Receipts

* **✔** sent
* **✔✔** delivered
* **✔✔ (blue)** read

### 🔔 Unread Message Count

Each room displays unread messages for the active user.

### 📨 Last Message Preview

Chat list shows last message + timestamp.

<<<<<<< HEAD
### 👥 Multi-user Mode

Switch between **any user** without login (simulation).

### 🧩 Clean Backend Architecture

* DRF API
* Channels for WebSocket
* Redis-backed message broadcasting
* Pagination for messages

---

# 🛠 5. **API Endpoints**

### **List Users**

=======
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
>>>>>>> 4bbb98e862e8c6a6d008917e2827da6a58931e2d

GET /api/users/


### **List Rooms (for active user)**


GET /api/rooms/?active_user=<id>


### **Create/Get Private Room**


POST /api/rooms/create/
{
  "user_id": <other_user>,
  "active_user_id": <me>
}

### **Get Messages**

GET /api/rooms/<room_id>/messages/



# 🔌 6. **WebSocket Wiring**

WebSocket Endpoint:

ws://127.0.0.1:8000/ws/chat/<room_id>/

<<<<<<< HEAD

### Events

| Event Type | Description            |
| ---------- | ---------------------- |
| `message`  | New chat message       |
| `typing`   | User typing indicator  |
| `read`     | Message marked as read |
=======
>>>>>>> 4bbb98e862e8c6a6d008917e2827da6a58931e2d

Events:

<<<<<<< HEAD

=======
Type	Description
message	New message
typing	User typing
read	Message marked read
>>>>>>> 4bbb98e862e8c6a6d008917e2827da6a58931e2d
