import "./css/homepage.css";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";

import animalsBg from "./assets/animals-background.jpg";
import animalsStatic from "./assets/animals-static.gif";
import animalsGif from "./assets/animals.gif";
import historyBg from "./assets/history-background.jpg";
import historyStatic from "./assets/history-static.gif";
import historyGif from "./assets/history.gif";
import entertainmentBg from "./assets/entertainment-background.jpg";
import entertainmentStatic from "./assets/entertainment-static.gif";
import entertainmentGif from "./assets/entertainment.gif";
import cultureBg from "./assets/culture-background.jpg";
import cultureStatic from "./assets/culture-static.gif";
import cultureGif from "./assets/culture.gif";

function App() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("Perspectify");

  const [appBackground, setAppBackground] = useState("default-bg");
  const [hoveredBox, setHoveredBox] = useState(null);

  const handleMouseEnter = (boxId, bgImage) => {
    setAppBackground(bgImage);
    setHoveredBox(boxId);
  };

  const handleMouseLeave = () => {
    setHoveredBox(null);
    setAppBackground(null);
  };

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
    <div
      className="app-background"
      style={{
        backgroundImage: appBackground ? `url(${appBackground})` : "none",
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        transition: "background 0.5s ease-in-out",
      }}
    >
      <div
        className="background-overlay"
        style={{
          backgroundImage: appBackground ? `url(${appBackground})` : "none", // Same as appBackground
          opacity: appBackground ? 1 : 0, // Fade effect for transitions
          transition: "opacity 0.5s ease-in-out",
        }}
      ></div>
      <div className="app">
        <div className="title">
          <h1>Perspectify</h1>
        </div>
        <div className="slogan">
          <p>"Learning through the perspectives of others"</p>
        </div>
        <div className="grid-container">
          <div className="row">
            <div
              className="square history"
              onClick={() => handleClick("History")}
              onMouseEnter={() => handleMouseEnter("history", historyBg)}
              onMouseLeave={handleMouseLeave}
              style={{
                backgroundImage: `url(${
                  hoveredBox === "history" ? historyGif : historyStatic
                })`,
                backgroundSize: "cover",
                backgroundPosition: "center",
                transition: "background-image 1s ease",
              }}
            >
              <p>History</p>
            </div>
            <div
              className="square animals"
              onClick={() => handleClick("Animals")}
              onMouseEnter={() => handleMouseEnter("animals", animalsBg)}
              onMouseLeave={handleMouseLeave}
              style={{
                backgroundImage: `url(${
                  hoveredBox === "animals" ? animalsGif : animalsStatic
                })`,
                backgroundSize: "cover",
                backgroundPosition: "center",
                transition: "background-image 1s ease",
              }}
            >
              <p>Animals</p>
            </div>
          </div>
          <div className="row">
            <div
              className="square entertainment"
              onClick={() => handleClick("Entertainment")}
              onMouseEnter={() =>
                handleMouseEnter("entertainment", entertainmentBg)
              }
              onMouseLeave={handleMouseLeave}
              style={{
                backgroundImage: `url(${
                  hoveredBox === "entertainment"
                    ? entertainmentGif
                    : entertainmentStatic
                })`,
                backgroundSize: "cover",
                backgroundPosition: "center",
                transition: "background-image 1s ease",
              }}
            >
              <p>Entertainment</p>
            </div>
            <div
              className="square culture"
              onClick={() => handleClick("Culture")}
              onMouseEnter={() => handleMouseEnter("culture", cultureBg)}
              onMouseLeave={handleMouseLeave}
              style={{
                backgroundImage: `url(${
                  hoveredBox === "culture" ? cultureGif : cultureStatic
                })`,
                backgroundSize: "cover",
                backgroundPosition: "center",
                transition: "background-image 1s ease",
              }}
            >
              <p>Culture</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
