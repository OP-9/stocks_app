import { useState } from "react";
import { service } from "../Service";

export default function SaveWB() {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      const data = await service.saveWB();
      //const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleClick}>
      {loading ? "Saving..." : "Save Workbook"}
    </button>
  );
}
