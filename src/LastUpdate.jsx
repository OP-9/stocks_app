import { useState } from "react";


export default function LastUpdate () {
    const [date, setDate] = useState(null);
    const [isHovering, setIsHovering] = useState(false)
    
    const handleMouseEnter = async () => {
        setIsHovering(true);
        try {
            const response = await fetch('http://localhost:5000/last_update');
            const data = await response.json();
            setDate(data.message);
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
        <p onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}>Last Updated on: {date? date: " Hover to get the date of the last portfolio update"}</p>
    </>
    )
}