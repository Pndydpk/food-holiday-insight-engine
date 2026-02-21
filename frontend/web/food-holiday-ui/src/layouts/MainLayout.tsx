import { Outlet } from "react-router-dom";
import TopNav from "../components/navigation/TopNav";

export default function MainLayout() {
  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      <TopNav />
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
