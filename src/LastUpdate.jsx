import { useState } from "react";


export default function LastUpdate () {
    const [date, setDate] = useState(null);
    const [portVal, setPortVal] = useState(null)
    const [invAmt, setInvAmt] = useState(null)
    const [portReturns, setPortReturns] = useState(null)
    const [portReturnsPerc, setPortReturnsPerc] = useState(null)
    const [isHovering, setIsHovering] = useState(false)
    
    const handleMouseEnter = async () => {
        setIsHovering(true);
        try {
            const response = await fetch('http://localhost:5000/last_update', 
                {method: 'GET'}
            );
            const data = await response.json();
            setDate(data.date_and_time);
            setPortVal(data.portfolio_value);
            setInvAmt(data.invested_amount);
            setPortReturns(data.portfolio_return);
            setPortReturnsPerc(data.portfolio_return_perc);
        } catch (error) {
            console.log("Error :", error)
            setDate("Unable to retrieve last update");
        } 
        };

    const handleMouseLeave = () => {
        setIsHovering(false);
        }

  return (
        <>
            <div> 
                <p onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}>Last Updated on: {date? date: " Hover to view the info \
                from when the Portfolio workbook was last updated. "}</p>
            </div>
            <div style={{display:"grid", gridTemplateColumns:"repeat(4, 1fr)"}}>
                <p>Portfolio Value</p>
                <p>Invested Amount</p>
                <p>Returns (₹)</p>
                <p>Returns (%)</p>    
            </div>
            <div style={{display:"grid", gridTemplateColumns:"repeat(4, 1fr)"}}>
                <p style={{marginTop:"0"}}>{portVal}</p>
                <p style={{marginTop:"0"}}>{invAmt}</p>
                <p style={{marginTop:"0"}}>{portReturns}</p>
                <p style={{marginTop:"0"}}>{portReturnsPerc}</p>    
            </div>
        </>
    )
}
