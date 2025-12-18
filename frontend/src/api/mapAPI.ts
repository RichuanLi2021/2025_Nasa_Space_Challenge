import axios from "axios";
import parsedEnv from "../config/env";

const api = axios.create({
  baseURL: `${parsedEnv.VITE_API_BASE}${parsedEnv.VITE_API_PREFIX}`,
  headers: {
    "ngrok-skip-browser-warning": "true"
  }
});

export default api;