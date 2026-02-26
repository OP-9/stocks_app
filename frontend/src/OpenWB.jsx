import { useState } from "react";
import { service } from "../Service";

export default function OpenWB() {
  const [loading, setLoading] = useState(false);
  const handleClick = async () => {
    setLoading(true);
    try {
      const data = await service.openWB();
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
      {loading ? "Opening..." : "Open Workbook"}
    </button>
  );
}
