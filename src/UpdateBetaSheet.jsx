import { useState } from "react";

export default function UpdateBetaSheet() {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/beta_sheet", {
        method: "POST",
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
      {loading ? "Updating Beta Sheet..." : "Update Beta Sheet"}
    </button>
  );
}
