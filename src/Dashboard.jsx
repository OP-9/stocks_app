import { useState } from "react";


export default function Dashboard () {
    const [clicked, setClicked] = useState(false);

    const handleClick = async () => { //Figure out how to make func recognise that link is open or closed
        if (clicked){
            setClicked(false)
        } else {
            setClicked(true)
        }

        /*try{
            const response = await fetch('http://localhost:5000/dashboard', {
                method:'POST'});
            const data = await response.json();
            alert(data.message);
        } catch (error){
            console.log("Error: ", error)
        }*/
        };

        return (
            <a onClick={handleClick}
                href="http://localhost:5000/dashboard" 
                target="_blank" 
                rel="noopener noreferrer">
                <button>Open Dashboard</button>
            </a>
        )
    };
