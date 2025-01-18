import React, {useState} from "react";
import "./css/option.css";
import { useNavigate, useLocation} from "react-router-dom";
import { FaCircleArrowRight } from "react-icons/fa6";

function App(){
    const location = useLocation();
    const title = location.state?.title || "Default Title";
    const [text, setText] = useState("");

    const handleChange = (event) => {
        setText(event.target.value);
      };
    const handleClick = () => {
        //Redirect to slide page or loading page while generate
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
                <input
                    type="text"
                    className="textbox"
                    value={text}
                    onChange={handleChange} 
                    placeholder="Type your question..."
                />
                <button className="icon-button"
                onClick={handleClick}
                disabled={!text} 
                >
                    <FaCircleArrowRight />
                </button>
            </div>
        </div>
    );
}

export default App;