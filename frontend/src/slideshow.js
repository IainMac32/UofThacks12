import "./css/slideshow.css";
import { useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";


function App() {
  const navigate = useNavigate();

  const [topic, setTopic] = useState([]); // 2-element array: [general topic, user's chosen person]
  const [people, setPeople] = useState({ names: [], descs: [], images: [] }); // Related people info
  const [info0, setInfo0] = useState([]); // Info and text log for one person
  const [info1, setInfo1] = useState([]); // Info and text log for one person
  const [info2, setInfo2] = useState([]); // Info and text log for one person
  const [info3, setInfo3] = useState([]); // Info and text log for one person
  const [currentPerson, setCurrentPerson] = useState(0); // Integer indicating the current person

  const [imageSrc, setImageSrc] = useState('https://via.placeholder.com/150'); // Placeholder image
  const [relationshipText, setRelationshipText] = useState('I am ___ I am related to this event/topic this way: ___');
  const [descriptionText, setDescriptionText] = useState('Initial description goes here.');

  const sendDataToBackend = () => {
    // Ensure the topic array has at least 2 elements
    if (topic.length < 2) {
      console.error("Topic array does not have enough elements.");
      return;
    }

    const user_topic = topic[0]; // The general topic
    const user_question = topic[1]; // The user's chosen input

    // Send data to the backend
    fetch("http://localhost:5000/api/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_topic: user_topic,
        user_question: user_question,
        past_response: "", // Initial value; not used here
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response from backend:", data.response);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const updatePastResponse = () => {
    // Decide which past_response to send based on currentPerson
    let past_response = "";
    switch (currentPerson) {
      case 0:
        past_response = info0.join(" ");
        break;
      case 1:
        past_response = info1.join(" ");
        break;
      case 2:
        past_response = info2.join(" ");
        break;
      case 3:
        past_response = info3.join(" ");
        break;
      default:
        console.error("Invalid currentPerson value");
        return;
    }

    // Send the past_response to the backend
    fetch("http://localhost:5000/api/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_topic: topic[0], // Send the current topic
        user_question: topic[1], // Send the current question
        past_response: past_response, // Send the selected past response
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Updated past_response response from backend:", data.response);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleClick = (option) => {
    console.log("TODO");
  };

  const handleBack = () => {
    navigate("/about");
  };
  // Placeholder functions to simulate arrow clicks and updates
  const handlePrevious = () => {
    // Update the state for the previous item
    setImageSrc('https://via.placeholder.com/150'); // Example new image
    setRelationshipText('Updated relationship text for previous');
    setDescriptionText('Updated description for previous.');
  };

  const handleNext = () => {
      // Update the state for the next item
      setImageSrc('https://via.placeholder.com/150'); // new image
      setRelationshipText('Updated relationship text for next');
      setDescriptionText('Updated description for next.');
  };

const [messages, setMessages] = useState([
    "Description, jdjjdjjdjjjdjjjdjjdnfkjnfjkerfernkjdsnkdlsfnkfwksjdnf. What more would you like to know?", // index 0 - response
    "w",
    "2",
    "2",
    "2",
    "2",
    "2",
    "2",
    "2",
    "2",
    "2"
]);
  
const [inputValue, setInputValue] = useState('');

const handleSendClick = () => {
  console.log(inputValue); // You can handle the input value here (e.g., send it to a server)
  setInputValue(''); // Clear the input field
};

  return (
    <div className="container">
      <div className="header">
        <div className="topic">
          <p>Chosen Topic</p>
          <p>{relationshipText}</p>
        </div>
      </div>

      <div className="middle-area">
        <div className="image-placeholder">
          <img src={imageSrc} alt="Topic" width="100%" />
        </div>

        <div className="grey-square">
          <div className="chat-container">
            <div className="message-log">
              {messages.map((message, index) => (
                <div 
                  key={index} 
                  className={`message ${index % 2 === 0 ? 'received' : 'sent'}`}>
                  {message}
                </div>
              ))}
            </div>
          </div>
          < div className="text-input-container">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              className="text-input"
            />
            <button onClick={handleSendClick} className="send-button">
              ↑
            </button>
          </div>
        </div>

      </div>
      <div className="navigation">
        <button className="nav-button" onClick={handlePrevious}>←</button>
        <button className="back-button" onClick={handleBack}>Back</button>
        <button className="nav-button" onClick={handleNext}>→</button>
      </div>
    </div>
    );
}

export default App;