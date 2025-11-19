import { useEffect, useState } from "react";
import api from "../services/api";
import UserList from "../components/UserList";
import ChatRoomList from "../components/ChatRoomList";
import { useNavigate } from "react-router-dom";

export default function Home({ userId, onLogout }) {
  const [users, setUsers] = useState([]);
  const [rooms, setRooms] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/users/").then((res) => setUsers(res.data));
  }, []);

  // auto refresh chat list
  useEffect(() => {
    const loadRooms = () => {
      api
        .get(`/rooms/`)
        .then((res) => setRooms(res.data));
    };

    loadRooms(); // first load

    const interval = setInterval(loadRooms, 1200);

    // also update on 'chat-updated' WS event
    window.addEventListener("chat-updated", loadRooms);

    return () => {
      clearInterval(interval);
      window.removeEventListener("chat-updated", loadRooms);
    };
  }, []);

  const startChat = (otherUserId) => {
    api
      .post("/rooms/create/", {
        user_id: otherUserId,
      })
      .then((res) => {
        navigate(`/chat/${res.data.id}`);
      });
  };

  return (
    <div className="h-screen flex">
      <div className="w-64 border-r bg-white flex flex-col">
        <div className="p-4 border-b">
          <h1 className="text-lg font-bold">Chat App</h1>
          <button onClick={onLogout} className="text-sm text-blue-500">Logout</button>
        </div>

        <ChatRoomList
          rooms={rooms}
          onSelect={(id) =>
            navigate(`/chat/${id}`)
          }
        />

        <UserList users={users} onSelect={startChat} />
      </div>

      <div className="flex-1 flex items-center justify-center text-gray-500">
        Select a chat or start a new one
      </div>
    </div>
  );
}
