import { NavLink } from "react-router-dom";

const navItems = [
  { label: "Command Center", path: "/" },
  { label: "Campaigns", path: "/campaigns" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-neutral-900 border-r border-neutral-800 p-4">
      <h1 className="text-xl font-bold mb-8">FoodLens</h1>

      <nav className="space-y-3">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }: { isActive: boolean }) =>
              `block px-3 py-2 rounded ${
                isActive ? "bg-purple-600" : "hover:bg-neutral-800"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
