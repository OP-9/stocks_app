import React, { useState } from 'react'
import './App.css'
import OpenWB from './OpenWb';
import SaveWB from './SaveWB';
import Dashboard from './Dashboard';
import UpdatePortfolio from './UpdatePortfolio';
import Transactions from './Transactions';
import UpdateLog from './UpdateLog';
import UpdateBetaSheet from './UpdateBetaSheet';
import UpdateSheets from './UpdateSheets';
import UpdateLedger from './UpdateLedger';
import LastUpdate from './LastUpdate';


const today = new Date();
const formattedDate = today.toLocaleDateString('en-GB');

function App(){


  return (
    <>
    <div>
      <h1>Stocks Portfolio</h1>
      <h3>Date: {formattedDate}</h3>
      <h3><LastUpdate/></h3>
    </div>
    <div>
        <OpenWB/>
        <Dashboard/>
        <SaveWB/>
    </div>
    <div>
        <UpdatePortfolio/>
        <Transactions/>
        <UpdateLog/>
    </div>
    <div>
      <UpdateBetaSheet/>
      <UpdateSheets/>
      <UpdateLedger/>
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
