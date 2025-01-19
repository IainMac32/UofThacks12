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








    const handleClick = (textInput) => {
        const payload = { topic: textInput }; // Create the payload

        fetch('https://flask-app-i7sgeivnqa-uc.a.run.app/api/getPerspectives', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                console.log('Success:', data);
                // Use the response data to navigate or update your UI
                navigate("/slideshow", { state: { response: data } });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };












    //Use API to replace this data
    const data=[
        {id:"1", question:"Question #1", link:"https://example.com"},
        {id:"2", question:"Question #2", link:"https://example.com"},
        {id:"3", question:"Question #3", link:"https://example.com"},
        {id:"4", question:"Question #4", link:"https://example.com"},
        {id:"5", question:"Question #5", link:"https://example.com"},
        {id:"6", question:"Question #6", link:"https://example.com"},
    ];
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
                onClick={() => handleClick(text)} 
                disabled={!text} 
                >
                <FaCircleArrowRight />
                </button>
            </div>
            <p className="similar-results-label"> Popular Questions</p>
            <div className="similar-results-table">
                {data.map((item) =>
                (<div className="table-row" key={item.id} >
                    <p>{item.id}.</p>
                    <a href={item.link}
                    target="_blank"
                    rel ="noopener noreferrer"
                    className="question-link"
                    >
                        {item.question}
                    </a>
                </div>
                ))}
            </div>
            </div>
        </div>
    );
}

export default App;