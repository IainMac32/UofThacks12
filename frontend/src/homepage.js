import "./css/homepage.css";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";

function App() {
    const navigate = useNavigate();
    const [ title, setTitle] = useState("Perspectify");

    const handleClick = (option) => {
        let newTitle;
        switch (option) {
          case "History":
            newTitle = "History";
            break;
          case "Animals":
            newTitle = "Animals";
            break;
          case "Entertainment":
            newTitle = "Entertainment";
            break;
          case "Culture":
            newTitle = "Culture";
            break;
          default:
            newTitle = "Perspectify";
        }
        setTitle(newTitle); 
        navigate("/about", { state: { title: newTitle } }); 
      };

  return (
    <div className="app-background">
      <div className="app">
        <div className="title">
          <h1>Perspectify</h1>
        </div>
        <div className="slogan">
          <p>"Learning through the perspectives of others"</p>
        </div>
        <div className="grid-container">
          <div className="row">
            <div className="square" onClick={() => handleClick("History")}>
              <p>History</p>
            </div>
            <div className="square" onClick={() => handleClick("Animals")}>
              <p>Animals</p>
            </div>
          </div>
          <div className="row">
            <div className="square" onClick={() => handleClick("Entertainment")}>
              <p>Entertainment</p>
            </div>
            <div className="square" onClick={() => handleClick("Culture")}>
              <p>Culture</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;