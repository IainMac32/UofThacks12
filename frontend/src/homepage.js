import "./css/homepage.css";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";

function App() {
    const navigate = useNavigate();
    const [ title, setTitle] = useState("Perspectify");

    const handleClick = (option) => {
        let newTitle;
        switch (option) {
          case "Option 1":
            newTitle = "Option 1";
            break;
          case "Option 2":
            newTitle = "Option 2";
            break;
          case "Option 3":
            newTitle = "Option 3";
            break;
          case "Option 4":
            newTitle = "Option 4";
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
            <div className="square" onClick={() => handleClick("Option 1")}>
              <p>Option 1</p>
            </div>
            <div className="square" onClick={() => handleClick("Option 2")}>
              <p>Option 2</p>
            </div>
          </div>
          <div className="row">
            <div className="square" onClick={() => handleClick("Option 3")}>
              <p>Option 3</p>
            </div>
            <div className="square" onClick={() => handleClick("Option 4")}>
              <p>Option 4</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;