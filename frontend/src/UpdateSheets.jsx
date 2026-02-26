import { useState } from "react";
import { service } from "../Service";

export default function UpdateSheets() {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);

    try {
      const data = await service.updateSheets();
      alert(data.message);
    } catch (error) {
      console.error("Error :", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <button onClick={handleClick}>
      {loading ? "Updating Sheets..." : "Update Sheets"}
    </button>
  );
}
