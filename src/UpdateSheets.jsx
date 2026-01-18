import { useState } from "react";

export default function UpdateSheets() {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/sheets", {
        method: "PUT",
      });

      const data = await response.json();
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
