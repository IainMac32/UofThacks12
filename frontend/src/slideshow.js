import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
function App (){
    const location = useLocation();
    const query = location.state?.query || "No query provided";
    useEffect(() => {
        if (query && query !== 'No query provided') {
          // Define the payload for the POST request
          const payload = { userQuery: query };
            console.log("Break-----------------------------");
          // Perform the POST request
          fetch('https://flask-app-i7sgeivnqa-uc.a.run.app/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          })
            .then((response) => response.json())
            .then((data) => {
              console.log('Success:', data);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        }
      }, [query]);
    
    return(
    <div>
        <center><h1>Slideshow Page</h1></center>
    </div>
    );
}

export default App; 