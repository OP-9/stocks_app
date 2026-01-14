import { useState } from "react";


export default function LastUpdate () {
    const [date, setDate] = useState(null);
    const [portVal, setPortVal] = useState(null)
    const [portReturns, setPortReturns] = useState(null)
    const [portReturnsPerc, setPortReturnsPerc] = useState(null)
    const [isHovering, setIsHovering] = useState(false)
    
    const handleMouseEnter = async () => {
        setIsHovering(true);
        try {
            const response = await fetch('http://localhost:5000/last_update');
            const data = await response.json();
            setDate(data.date_and_time);
            setPortVal(data.portfolio_value);
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
            onMouseLeave={handleMouseLeave}>Last Updated on: {date? date: " Hover to get the date of the last portfolio update"}</p>
        </div>
        <div style={{display:"grid", gridTemplateColumns:"repeat(3, 1fr)"}}>
            <p>Portfolio Value: {portVal}</p>
            <p>Returns (₹): {portReturns}</p>
            <p>Returns (%): {portReturnsPerc}</p>    
        </div>
    </>
    )
}
