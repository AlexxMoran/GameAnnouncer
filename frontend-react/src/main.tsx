import { App } from "@app/index";
import dayjs from "dayjs";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";

dayjs.extend(utc);
dayjs.extend(timezone);

const root = document.getElementById("root");

createRoot(root!).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
