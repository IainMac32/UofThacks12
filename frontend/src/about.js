import React from 'react';

import "./css/homepage.css";
import { useNavigate, useLocation } from "react-router-dom";

function App(){
    const location = useLocation();
    const title = location.state?.title || "Default Title";
    
    return(
        <div>
            <h1>{title}</h1>
        </div>
    );
}

export default App;