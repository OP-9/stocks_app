import { useState } from "react";
import { useEffect } from "react";

export default function LastUpdate({ update, resetUpdate }) {
  const [date, setDate] = useState(null);
  const [portVal, setPortVal] = useState(null);
  const [invAmt, setInvAmt] = useState(null);
  const [portReturns, setPortReturns] = useState(null);
  const [portReturnsPerc, setPortReturnsPerc] = useState(null);

  useEffect(() => {
    const mainFunc = async () => {
      try {
        const response = await fetch("http://localhost:5000/last_update", {
          method: "GET",
        });
        const data = await response.json();
        console.log(data.message);
        setDate(data.date_and_time);
        setPortVal(data.portfolio_value);
        setInvAmt(data.invested_amount);
        setPortReturns(data.portfolio_return);
        setPortReturnsPerc(data.portfolio_return_perc);
      } catch (error) {
        console.log("Error :", error);
        setDate("Unable to retrieve last update");
      } finally {
        resetUpdate();
      }
    };

    mainFunc();
  }, [update]);

  return (
    <>
      <div>
        <p>
          Last Updated on:{" "}
          {date
            ? date
            : "Click on Update Portfolio \
                    to preview portfolio info"}
        </p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)" }}>
        <p>Portfolio Value</p>
        <p>Invested Amount</p>
        <p>Returns (₹)</p>
        <p>Returns (%)</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)" }}>
        <p style={{ marginTop: "0" }}>{portVal}</p>
        <p style={{ marginTop: "0" }}>{invAmt}</p>
        <p style={{ marginTop: "0" }}>{portReturns}</p>
        <p style={{ marginTop: "0" }}>{portReturnsPerc}</p>
      </div>
    </>
  );
}
