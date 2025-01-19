import "./css/slideshow.css";
import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

function App() {
  const navigate = useNavigate();
  
  const location = useLocation();
  const data = location.state?.response || {}; // Retrieve the 'response' key, which is the data


  const [topic, setTopic] = useState([]); // 2-element array: [general topic, user's chosen person]
  const [data1, setPeople] = useState(data);
  const [info0, setInfo0] = useState([data1.descs[0]]); // Separate elements in the array
  const [info1, setInfo1] = useState([data1.descs[1]]); // Info and text log for one person
  const [info2, setInfo2] = useState([data1.descs[2]]); // Info and text log for one person
  const [info3, setInfo3] = useState([data1.descs[3]]); // Info and text log for one person
  const [currentPerson, setCurrentPerson] = useState(0); // Integer indicating the current person

  const [imageSrc, setImageSrc] = useState(data1.images[currentPerson]); // Placeholder image
  const [relationshipText, setRelationshipText] = useState("I am " + data1.names[currentPerson]);

  let info
  if (currentPerson === 0) {
    info = info0;
  } else if (currentPerson === 1) {
    info = info1;
  } else if (currentPerson === 2) {
    info = info2;
  } else if (currentPerson === 3) {
    info = info3;
  }

  const [descriptionText, setDescriptionText] = useState(info);


  const appendString = (newString) => {
    switch (currentPerson) {
      case 0:
        setInfo0([...info0, newString]);
        break;
      case 1:
        setInfo1([...info1, newString]);
        break;
      case 2:
        setInfo2([...info2, newString]);
        break;
      case 3:
        setInfo3([...info3, newString]);
        break;
      default:
        console.error("Invalid person index");
    }
  };




  const sendDataToBackend = () => {
    if (topic.length < 2) {
      console.error("Topic array does not have enough elements.");
      return;
    }

    const user_topic = topic[0]; // The general topic
    const user_question = topic[1]; // The user's chosen input

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

    fetch("http://localhost:5000/api/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_topic: topic[0],
        user_question: topic[1],
        past_response: past_response,
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

  const handlePrevious = () => {
    setCurrentPerson((prevPerson) => {
      const prevPersonIndex = (prevPerson - 1 + data1.names.length) % data1.names.length;
      setDescriptionText(data1.descs[prevPersonIndex]);
      setImageSrc(data1.images[prevPersonIndex]);
      setRelationshipText(`I am ${data1.names[prevPersonIndex]}`);
      
      // Update messages with previous description
      setMessages((prevMessages) => [data1.descs[prevPersonIndex]]);

      return prevPersonIndex;
    });
  };

  const handleNext = () => {
    setCurrentPerson((prevPerson) => {
      const nextPerson = (prevPerson + 1) % data1.names.length;
      setDescriptionText(data1.descs[nextPerson]);
      setImageSrc(data1.images[nextPerson]);
      setRelationshipText(`I am ${data1.names[nextPerson]}`);

      // Update messages with next description
      setMessages((prevMessages) => [data1.descs[nextPerson]]);
      
      return nextPerson;
    });
  };

  const [messages, setMessages] = useState([
    descriptionText, // index 0 - response
  ]);

  const [inputValue, setInputValue] = useState('');

  const handleSendClick = () => {
    console.log(inputValue);
    // Add inputValue to the messages list, keeping previous messages intact
  
    appendString(inputValue);

    // Clear the input field
    setInputValue('');

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
          <img src={imageSrc} alt="Topic" width="80%" />
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
          <div className="text-input-container">
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
