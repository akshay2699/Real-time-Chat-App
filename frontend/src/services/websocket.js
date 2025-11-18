// src/services/websocket.js
export class ChatSocket {
  constructor(roomId, onMessage) {
    this.roomId = roomId;
    this.onMessage = onMessage;
    this.connect();
  }

  connect() {
    const url = `ws://127.0.0.1:8000/ws/chat/${this.roomId}/`;
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log("WS Connected:", this.roomId);
    };

    this.socket.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        this.onMessage(data);
      } catch (err) {
        console.error("WS parse error:", err, e.data);
      }
    };

    this.socket.onclose = (e) => {
      console.log("WS closed", e);
    };

    this.socket.onerror = (err) => {
      console.log("WS Error", err);
    };
  }

  // payload: { text, sender_id }
  sendMessage({ text, sender_id }) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.warn("Socket not open - message not sent");
      return;
    }
    this.socket.send(
      JSON.stringify({
        type: "message",
        text,
        sender_id,
      })
    );
  }

  // sender_id: number
  sendTyping(sender_id) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
    this.socket.send(
      JSON.stringify({
        type: "typing",
        sender_id,
      })
    );
  }

  // message_id: number
  sendRead(message_id) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
    this.socket.send(
      JSON.stringify({
        type: "read",
        message_id,
      })
    );
  }
}
