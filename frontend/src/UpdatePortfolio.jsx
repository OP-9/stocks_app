import { useState } from "react";
import { service } from "../Service";

export default function UpdatePortfolio({ onUpdate }) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      const data = await service.updatePortfolio();
      alert(data.message);
    } catch (error) {
      if (error.response) {
        alert(`Error:  ${error.response.data.message}`);
      }
      console.error("Error: ", error);
    } finally {
      setLoading(false);
      onUpdate();
    }
  };

  return (
    <button onClick={handleClick}>
      {loading ? "Updating..." : " Update Portfolio"}
    </button>
  );
}
