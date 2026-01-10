import React, { useState } from 'react'
import './App.css'
import OpenWB from './OpenWb';
import SaveWB from './SaveWB';


function App(){

  
  return (
    <>
    <div>
      <h1>Stocks Portfolio</h1>
      <h3>Date</h3>
      <h3>Last Updated</h3>
    </div>
    <div>
      <>
      <OpenWB/>
      </>
      <button>
        <p>Dashboard</p>
      </button>
      <>
      <SaveWB/>
      </>
    </div>

    <div>
      <button>
        <p>Update Portfolio</p>
      </button>
      <button>
        <p>Transaction</p>
      </button>
      <button>
        <p>Update Log</p>
      </button>
    </div>
    <div>
      <button>
        <p>Update Beta Sheet</p>
      </button>
      <button>
        <p>Update Sheet</p>
      </button>
      <button>
        <p>Update Ledger</p>
      </button>
    </div>
    </>
  )
}


/*
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <div>
        <button>
        <h2>Just testing this</h2>
        </button>
      </div>
    </>
  )
}
*/


export default App
