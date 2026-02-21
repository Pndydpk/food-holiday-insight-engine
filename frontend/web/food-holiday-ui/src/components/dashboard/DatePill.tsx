type DatePillProps = {
  date: Date;
  onClick: () => void;
  isActive?: boolean;
  isMajor?: boolean; 
};

export default function DatePill({ date, onClick, isActive, isMajor }: DatePillProps) {
  const month = date.toLocaleString("en-US", { month: "short" }).toUpperCase();
  const day = date.getDate();

  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        flex flex-col items-center justify-center relative
        w-20 h-24 rounded-2xl border-2 transition-all duration-300
        ${isActive 
          ? "border-pink-500 bg-pink-500/20 shadow-[0_0_20px_rgba(236,72,153,0.4)]" 
          : "border-white/10 bg-black/60 backdrop-blur-md hover:border-pink-500"}
      `}
    >
      <span className="text-[11px] font-black tracking-widest text-pink-500 mb-1">{month}</span>
      <span className="text-3xl font-black text-white leading-none">{day}</span>
      
      {/* PROFIT SIGNAL: Neon Blue Underscore for Major Holidays */}
      {isMajor && (
        <div className="absolute -bottom-1 w-10 h-1 bg-cyan-400 rounded-full shadow-[0_0_12px_rgba(34,211,238,1)]" />
      )}
    </button>
  );
}