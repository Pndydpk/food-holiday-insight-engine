type Props = {
  label: string;
  value: string;
  accent?: "green" | "yellow" | "pink";
};

const accentMap = {
  green: "border-l-emerald-500 text-emerald-400",
  yellow: "border-l-yellow-400 text-yellow-300",
  pink: "border-l-pink-500 text-pink-400",
};

export default function MetricCard({ label, value, accent = "green" }: Props) {
  return (
    <div
      className={`
        bg-neutral-900
        border border-neutral-800
        border-l-4 ${accentMap[accent]}
        rounded-xl
        p-5
      `}
    >
      <p className="text-xs uppercase tracking-wide text-neutral-500">
        {label}
      </p>
      <p className="mt-2 text-2xl font-semibold text-white">
        {value}
      </p>
    </div>
  );
}
