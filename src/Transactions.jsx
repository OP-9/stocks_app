import { useState } from "react";

export default function Transactions () {
    const [clicked, setClicked] = useState(false);
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({
    date: "",
    symbol: "",
    action: "",
    quantity: "",
    price:""
  });

  // Handle changes for all inputs dynamically
  const handleClick = () => {
    if (clicked){
      setClicked(false);
    } else{
      setClicked(true);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    setLoading(true);
    if (clicked) {
    e.preventDefault();
        try{
        const response = await fetch('http://localhost:5000/transaction', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData) 
        });

        const data = await response.json();
        alert(data.message);
      } catch (error){ 
        console.log("Error: ", error)
      } finally {
        setClicked(false);
        setLoading(false);
      }
      }
      };

  return (
    <>
    {clicked?(
      <form style={{display: "flex", flexDirection: "column"}}>
      <input name="date" placeholder="Date: Enter date of purchase in dd/mm/yyyy format" onChange={handleChange}></input>
      <input name="symbol" placeholder="Symbol: Enter the stock symbol" onChange={handleChange}></input>
      <input name="action" placeholder="Action: Enter the action, i.e., either a BUY or SELL:" onChange={handleChange}></input>
      <input name="quantity" placeholder="Quantity: Enter the quantity" onChange={handleChange}></input>
      <input name="price" placeholder="Price: Enter the price of the stock" onChange={handleChange}></input>
      <button onClick={handleSubmit}>{loading?"Submitting...":"Submit"}</button>
      <button onClick={handleClick}>{loading?"Cancelling...":"Cancel"}</button>
      </form>
      )
      :<button onClick={handleClick}>Transactions</button>}
    </>
  );
};
