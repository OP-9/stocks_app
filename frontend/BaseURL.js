import axios from "axios";

const baseURL = axios.create({
  baseURL: "http://localhost:5001",
});

export default baseURL;
