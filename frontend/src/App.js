import "./App.css";

const handleClick = (option) =>{
  console.log("TODO");
}

function App() {
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
