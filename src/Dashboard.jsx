export default function Dashboard() {
  return (
    <a
      id="dashboard_link"
      href="http://localhost:5000/dashboard"
      target="_blank"
      rel="noopener noreferrer"
      style={{ margin: "2em", maxHeight: "58px" }}
    >
      <button id="open_dash_button" style={{ margin: 0 }}>
        Open Dashboard
      </button>
    </a>
  );
}
