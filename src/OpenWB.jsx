import { useState } from "react";

export default function OpenWB() {
    const [loading, setLoading] = useState(false);
  const handleClick= async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/open_wb', {
        method: 'POST',
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
      <button onClick={handleClick} style={{margin: "2em", padding: "2em"}}>
        {loading? "Opening..." : "Open Workbook"}
      </button>
  );
}


