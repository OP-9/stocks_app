import { useState } from "react";

export default function UpdatePortfolio ({onUpdate}) {
    const [loading, setLoading] = useState(false);

    const handleClick = async () => {
        setLoading(true)
        try{
            const response = await fetch ('http://localhost:5000/update_portfolio', {
        method: 'PUT',
        });
        const data = await response.json();
        alert(data.message)
        } catch (error){
            console.log("Error: ", error)
        }
        finally{
            setLoading(false)
            onUpdate()
        }
    };

    return (
      <button onClick={handleClick}>
        {loading? "Updating..." : " Update Portfolio"}
      </button>
  );
};