import './App.css'
import OpenWB from './OpenWB';
import SaveWB from './SaveWB';
import Dashboard from './Dashboard';
import UpdatePortfolio from './UpdatePortfolio';
import Transactions from './Transactions';
import UpdateLog from './UpdateLog';
import UpdateBetaSheet from './UpdateBetaSheet';
import UpdateSheets from './UpdateSheets';
import UpdateLedger from './UpdateLedger';
import LastUpdate from './LastUpdate';
import { useState } from 'react';


const today = new Date();
//const formattedDate = today.toLocaleDateString('en-GB');

const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
const longDate = new Intl.DateTimeFormat('en-GB', options).format(today)

function App(){

  const [update, setUpdate] =useState(false);

  const onUpdate = () => {
    setUpdate(true)
  };


  return (
    <>
      <div style={{gridArea:'titles',}}>
        <h1>Portfolio</h1>
        <h3>{longDate}</h3>
        <><LastUpdate update = {update} resetUpdate={() => setUpdate(false)}/></> 
      </div>
      <div className='container'>
        <div className='box' style={{display:'flex', flexDirection:'column'}}>
            <OpenWB/>
            <UpdatePortfolio onUpdate={onUpdate}/>
            <UpdateSheets/>
        </div>
        <div className='box' style={{display:'flex', flexDirection:'column'}}>
            <Dashboard/>
            <UpdateLog/>
            <Transactions/>
        </div>
        <div className='box' style={{display:'flex', flexDirection:'column'}}>
          <SaveWB/>
          <UpdateBetaSheet/>
          <UpdateLedger/>
        </div>
      </div>
    </>
  )
}


export default App
