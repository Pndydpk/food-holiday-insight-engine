type Props = {
  selectedDate: Date;
  onSelect: (date: Date) => void;
  onClose: () => void;
};

export default function CalendarPopover({
  selectedDate,
  onSelect,
  onClose,
}: Props) {
  const days = Array.from({ length: 31 }, (_, i) => {
    const d = new Date(selectedDate);
    d.setDate(i + 1);
    return d;
  });

  return (
    <div
      className="
        fixed
        top-[140px]
        left-[140px]
        z-[99999]
        bg-neutral-900
        border border-neutral-700
        rounded-xl
        p-4
        w-72
        shadow-2xl
      "
    >
      <div className="grid grid-cols-7 gap-2">
        {days.map((date) => (
          <button
            key={date.toISOString()}
            onClick={() => {
              onSelect(date);
              onClose();
            }}
            className="
              h-9 rounded-md
              text-sm text-neutral-300
              hover:bg-neutral-800
            "
          >
            {date.getDate()}
          </button>
        ))}
      </div>
    </div>
  );
}
