type DatePillProps = {
  date: Date;
  onClick: () => void;
};

export default function DatePill({ date, onClick }: DatePillProps) {
  const month = date
    .toLocaleString("en-US", { month: "short" })
    .toUpperCase();

  const day = date.getDate();

  return (
    <button
      type="button"
      onClick={onClick}
      className="
        flex flex-col items-center justify-center
        w-14 h-16
        rounded-lg
        border border-neutral-700
        bg-neutral-900
        transition-all duration-200
        hover:border-pink-500
        hover:bg-pink-500/10
        focus:outline-none
      "
      aria-label="Select date"
    >
      <span className="text-[10px] tracking-wider text-neutral-400">
        {month}
      </span>

      <span className="text-xl font-semibold text-white leading-none">
        {day}
      </span>
    </button>
  );
}
