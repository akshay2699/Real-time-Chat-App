import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [userId, setUserId] = useState(localStorage.getItem("userId"));

  const handleLogin = (newToken, newUserId) => {
    localStorage.setItem("token", newToken);
    localStorage.setItem("userId", newUserId);
    setToken(newToken);
    setUserId(newUserId);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    setToken(null);
    setUserId(null);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            token ? (
              <Home userId={userId} onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/login"
          element={!token ? <LoginPage onLogin={handleLogin} /> : <Navigate to="/" />}
        />
        <Route
          path="/chat/:roomId"
          element={token ? <ChatPage /> : <Navigate to="/login" />}
        />
      </Routes>
    </BrowserRouter>
  );
}
