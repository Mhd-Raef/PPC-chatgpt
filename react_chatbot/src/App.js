import React, { useEffect, useState } from 'react';

const App = () => {
  const [csrfToken, setCsrfToken] = useState('');
  const [messages, setMessages] = useState([
    {
      sender: 'AI Chatbot',
      content: 'Hi, I am your AI Chatbot, you can ask me anything. Write (RESET) to reset context',
      type: 'received'
    }
  ])
  const [messageInput, setMessageInput] = useState('')

  
  useEffect(() => {
    async function fetchCsrfToken() {
      try {
        const response = await fetch('/api/csrf_token/')
        const data = await response.json()
        setCsrfToken(data.csrfToken)
      } catch (error) {
        console.error('Error retrieving CSRF token:', error)
      }
    }
    fetchCsrfToken()
  }, [])

  function fetchResponse(){
    fetch('',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken
      },
      body: new URLSearchParams({
        'message': messageInput
      })
    }) 
    .then(response => response.json())
    .then(data => {
      const resData = data.response
      const newMessage = {
        sender: 'AI Chatbot',
        content: resData,
        type: 'received'
      }
      setMessages(messages => [...messages, newMessage])
    })
  }

  useEffect(() => {
    if (messageInput.trim().length > 0) {
      fetchResponse();
    }
  },[])

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    
    const message = messageInput.trim();
    if (message.length === 0) {
      return;
    }
    
    const newMessage = {
      sender: 'You',
      content: message,
      type: 'sent'
    }
    setMessages(messages => [...messages, newMessage])
    setMessageInput('')

    fetchResponse()
  }

  return (
    <div className="chat-container">
      <div className="">
        <div className="header-text">Chatgpt with Security Powers</div>
        <div className="messages-box">
          <ul className="list-unstyled messages-list">
            {messages.map((message, index) => (
              <li className={`message ${message.type}`} key={index}>
                <div className="message-text">
                  <div className="message-sender">
                    <b>{message.sender}</b>
                  </div>
                  <div className="message-content">
                    {message.content}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <br /><br />
        <br /><br />
        <br /><br />
      </div>
      <form className="message-form" onSubmit={handleFormSubmit}>
        <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
        <input
          type="text"
          className=" message-input"
          placeholder="Type your message..."
          value={messageInput}
          onChange={(e) => setMessageInput(e.target.value)}
        />
        <button type="submit" className="btn-send">Send</button>
      </form>
    </div>
  )
}

export default App;
