import { createBrowserRouter } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import DashboardPage from "../pages/Dashboard/DashboardPage";

export const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      { path: "/", element: <DashboardPage /> },
    ],
  },
]);
