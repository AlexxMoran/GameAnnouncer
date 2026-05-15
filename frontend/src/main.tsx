import { router } from "@app/routes";
import dayjs from "dayjs";
import "dayjs/locale/ru";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router";

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("ru");

const root = document.getElementById("root");

createRoot(root!).render(<RouterProvider router={router} />);
