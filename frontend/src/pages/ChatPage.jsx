import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import ChatWindow from "../components/ChatWindow";
import { ChatSocket } from "../services/websocket";

export default function ChatPage() {
  const { roomId } = useParams();
  const activeUser = Number(localStorage.getItem("userId"));

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [typing, setTyping] = useState(false);
  const [currentUser, setCurrentUser] = useState("");

  const socketRef = useRef(null);

  // load users + set current user
  useEffect(() => {
    api.get("/users/").then((res) => {
      const me = res.data.find((u) => u.id === activeUser);
      if (me) setCurrentUser(me.username);
    });
  }, [activeUser]);

  // load chat history
  useEffect(() => {
    api.get(`/rooms/${roomId}/messages/`).then((res) => {
      setMessages(res.data.results.reverse());
    });
  }, [roomId]);

  // setup websocket
  useEffect(() => {
    const socket = new ChatSocket(roomId, handleSocket);
    socketRef.current = socket;

    return () => {
      if (socketRef.current) {
        socketRef.current.socket.close();
      }
    };
  }, [roomId]);

  // handle websocket events
  const handleSocket = (data) => {
    if (data.type === "message") {
      setMessages((prev) => [...prev, data.message]);
      window.dispatchEvent(new Event("chat-updated"));
      return;
    }

    if (data.type === "typing") {
      if (data.user_id !== activeUser) {
        setTyping(true);
        setTimeout(() => setTyping(false), 1200);
      }
      return;
    }

    if (data.type === "read") {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === data.message_id ? { ...m, is_read: true } : m
        )
      );
      window.dispatchEvent(new Event("chat-updated"));
      return;
    }
  };

  // send message
  const sendMessage = () => {
    if (!text.trim()) return;

    const msg = text;
    setText("");

    socketRef.current.sendMessage({
      text: msg,
    });

    // optimistic UI
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        text: msg,
        sender: { id: activeUser, username: currentUser },
        receiver: null,
        timestamp: new Date().toISOString(),
        is_read: false,
      },
    ]);
  };

  // mark unread as read
  useEffect(() => {
    const unread = messages.filter(
      (m) => m.receiver?.id === activeUser && !m.is_read
    );

    unread.forEach((m) => socketRef.current.sendRead(m.id));
  }, [messages]);

  return (
    <div className="h-screen">
      <ChatWindow
        messages={messages}
        typing={typing}
        text={text}
        setText={setText}
        onSend={sendMessage}
        onTyping={() => socketRef.current.sendTyping()}
        currentUser={currentUser}
      />
    </div>
  );
}
