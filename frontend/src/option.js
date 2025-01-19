import React, {useState} from "react";
import "./css/option.css";
import { useNavigate, useLocation} from "react-router-dom";
import { FaCircleArrowRight } from "react-icons/fa6";

function App(){
    const location = useLocation();
    const title = location.state?.title || "Default Title";
    const [text, setText] = useState("");
    const navigate = useNavigate();
    const handleChange = (event) => {
        setText(event.target.value);
      };
    const handleClick = () => {
        navigate("/slideshow");
      }
    return(
        <div className='option-page'>
            <div className="option-title">
                <h1>Perspectify</h1>
            </div>
            <div className='option-question'>
                <h3>What would you like to know about {title}?</h3>
            </div>
            <div>
            <div className="input-container">
                <input
                    type="text"
                    className="textbox"
                    value={text}
                    onChange={handleChange} 
                    placeholder="Type your question..."
                />
                <button className={`continue-but ${text ? "active" : "disabled"}`}
                onClick={handleClick}
                disabled={!text} 
                >
                    <FaCircleArrowRight />
                </button>
            </div>
            </div>
        </div>
    );
}

export default App;