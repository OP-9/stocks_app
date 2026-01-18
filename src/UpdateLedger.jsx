import { useState } from "react";

export default function UpdateLedger() {
  const [loading, setLoading] = useState(false);
  const [canceled, setCanceled] = useState(false);
  const [clicked, setClicked] = useState(false);

  const [formData, setFormData] = useState({
    timePeriod: "",
    arunBhatia: "",
    babitaBhatia: "",
    aakashBhatia: "",
    shikharBhatia: "",
    ajayBhatia: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleCancel = () => {
    if (canceled) {
      setCanceled(true);
      setLoading(true);
    }
  };

  const handleClick = () => {
    if (clicked) {
      setClicked(false);
    } else {
      setClicked(true);
    }
  };

  const handleSubmit = async (e) => {
    setLoading(true);

    e.preventDefault();
    if (clicked) {
      try {
        const response = await fetch("http://localhost:5000/ledger", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        });
        const data = await response.json();
        alert(data.message);
      } catch (error) {
        console.error("Error :", error);
      } finally {
        setLoading(false);
        setClicked(false);
      }
    }
  };
  return (
    <>
      {clicked ? (
        <form style={{ display: "flex", flexDirection: "column" }}>
          <p style={{ textAlign: "left" }}>
            If an investor has paid, add the amount that they have paid. If they
            haven't paid, input the amount as 0
          </p>
          <input
            onChange={handleChange}
            name="timePeriod"
            placeholder="Enter the period in the following format Aug-24"
          ></input>
          <input
            name="Investor1"
            placeholder="Investor1"
            onChange={handleChange}
          ></input>
          <input
            name="Investor2"
            placeholder="Investor2"
            onChange={handleChange}
          ></input>
          <input
            name="Investor3"
            placeholder="Investor3"
            onChange={handleChange}
          ></input>
          <input
            name="Investor4"
            placeholder="Investor4"
            onChange={handleChange}
          ></input>
          <input
            name="Investor5"
            placeholder="Investor5"
            onChange={handleChange}
          ></input>
          <button id="submit_button" onClick={handleSubmit}>
            {loading && !canceled ? "Submitting..." : "Submit"}
          </button>
          <button id="cancel_button" onClick={handleCancel}>
            {loading && canceled ? "Canceling..." : "Cancel"}
          </button>
        </form>
      ) : (
        <button onClick={handleClick}>Update Ledger</button>
      )}
    </>
  );
}
