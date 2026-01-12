import { useState } from "react";

export default function Dashboard () {
    const [open, setOpen] = useState(false);

    const handleClick = async () => {
        try{
            const response = await fetch('http://localhost:5000/dashboard', {
                method:'POST'});
            const data = response.json();
            alert(data.message);
        } catch (error){
            console.log("Error: ", error)
        }   finally {
            if (open){
            setOpen(false)
            }  else {
            setOpen(true)
            }
        }
        };

        return (
            <button onClick={handleClick}>
                {open?"Close Dashboard":"Open Dashboard"}
            </button>
        )
    };
