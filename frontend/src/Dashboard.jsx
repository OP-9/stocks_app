export default function Dashboard() {
  return (
    <a
      /* Use port 5001 to reach  Docker backend */
      href="http://localhost:5001/dashboard"
      target="_blank"
      rel="noopener noreferrer"
      style={{ margin: "2em", display: "inline-block" }}
    >
      <button id="open_dash_button" style={{ margin: 0 }}>
        Open Dashboard
      </button>
    </a>
  );
}
