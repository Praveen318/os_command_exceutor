import React, { useState } from 'react';
import './App.css';

function App() {
  const [userPrompt, setUserPrompt] = useState('');
  const [command, setCommand] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const executeCommand = async () => {
    setError(null);
    setResult(null);
    setCommand('');

    try {
      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_prompt: userPrompt,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setCommand(data.command);
        setResult(data.result);
      } else {
        setError(data.detail);
      }
    } catch (err) {
      setError('Error executing command');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>OS Command Executor</h1>
        <textarea
          className="input-box"
          placeholder="Enter your command..."
          value={userPrompt}
          onChange={(e) => setUserPrompt(e.target.value)}
        />
        <button className="execute-button" onClick={executeCommand}>Execute</button>
        {command && <div className="output-box">Command: {command}</div>}
        {result && <div className="output-box">Result: {result}</div>}
        {error && <div className="error-box">Error: {error}</div>}
      </header>
    </div>
  );
}

export default App;
// import React, { useState } from 'react';
// import './App.css';

// function App() {
//   const [userPrompt, setUserPrompt] = useState('');
//   const [command, setCommand] = useState('');
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState(null);
//   const [solution, setSolution] = useState('');
//   const [solutionResult, setSolutionResult] = useState('');

//   const executeCommand = async () => {
//     setError(null);
//     setResult(null);
//     setCommand('');
//     setSolution('');
//     setSolutionResult('');

//     try {
//       const response = await fetch('http://localhost:8000/execute', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           user_prompt: userPrompt,
//         }),
//       });

//       const data = await response.json();

//       if (response.ok) {
//         setCommand(data.command);
//         setResult(data.result);
//         if (data.solution) {
//           setSolution(data.solution);
//           setSolutionResult(data.solution_result);
//         }
//       } else {
//         setError(data.detail);
//       }
//     } catch (err) {
//       setError('Error executing command');
//     }
//   };

//   return (
//     <div className="App">
//       <header className="App-header">
//         <h1>OS Command Executor</h1>
//         <textarea
//           className="input-box"
//           placeholder="Enter your command..."
//           value={userPrompt}
//           onChange={(e) => setUserPrompt(e.target.value)}
//         />
//         <button className="execute-button" onClick={executeCommand}>Execute</button>
//         {command && <div className="output-box">Command: {command}</div>}
//         {result && <div className="output-box">Result: {result}</div>}
//         {error && <div className="error-box">Error: {error}</div>}
//         {solution && <div className="output-box">Solution Attempted: {solution}</div>}
//         {solutionResult && <div className="output-box">Solution Result: {solutionResult}</div>}
//       </header>
//     </div>
//   );
// }

// export default App;
