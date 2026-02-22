import React, { useState } from 'react';
import DatePill from './DatePill';

const HOLIDAY_DATABASE: Record<string, any> = {
  "2026-02-08": {
    name: "National Potato Chip Day",
    isMajor: true,
    image: "https://images.unsplash.com/photo-1566478431370-763b197a6616?auto=format&fit=crop&q=80&w=1200",
    color: "from-orange-400 to-pink-500",
    viral: "9.4",
    revenue: "12.4k"
  },
  "2026-02-14": {
    name: "Valentine's Day Dessert",
    isMajor: true,
    image: "https://images.unsplash.com/photo-1518133835878-5a93cc3f89e5?auto=format&fit=crop&q=80&w=1200",
    color: "from-red-500 to-pink-600",
    viral: "9.9",
    revenue: "24.1k"
  }
};

const HeroSpotlight: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState(new Date("2026-02-08"));
  const [showCalendar, setShowCalendar] = useState(false);
  
  const dateKey = selectedDate.toISOString().split('T')[0];
  const activeData = HOLIDAY_DATABASE[dateKey] || {
    name: "Food Insight Day",
    isMajor: false,
    image: "https://images.unsplash.com/photo-1495147466023-ac5c588e2e94?auto=format&fit=crop&q=80&w=1200",
    color: "from-zinc-400 to-zinc-200",
    viral: "4.2",
    revenue: "1.8k"
  };

  return (
    <div className="p-10 bg-black min-h-screen text-white">
      <div className="flex items-center gap-3 mb-10">
        <h2 className="text-4xl font-black uppercase italic tracking-tighter">Hero Spotlight</h2>
        <div className="h-px grow bg-white/5 ml-4" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        
        {/* MAIN HERO CARD */}
        <div className="lg:col-span-8 relative rounded-[40px] border border-white/10 bg-[#0a0a0c] overflow-hidden min-h-[560px] flex flex-col shadow-2xl">
          <div className="absolute inset-0 z-0">
            <img 
              key={activeData.image}
              src={activeData.image} 
              className="w-full h-full object-cover opacity-50 transition-opacity duration-500"
              alt="Holiday Backdrop"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-black via-black/40 to-transparent" />
          </div>

          <div className="relative z-10 p-12 flex flex-col h-full grow justify-between">
            <div className="relative inline-block">
              <DatePill 
                date={selectedDate} 
                isMajor={activeData.isMajor} 
                isActive={showCalendar} 
                onClick={() => setShowCalendar(!showCalendar)} 
              />
              {showCalendar && (
                <div className="absolute top-28 left-0 z-50 bg-[#0d0d0f] border-2 border-pink-500 p-6 rounded-3xl shadow-[0_0_40px_rgba(236,72,153,0.3)]">
                  <input 
                    type="date" 
                    className="bg-zinc-900 text-white p-3 rounded-xl border border-white/10 outline-none"
                    style={{ colorScheme: 'dark' }}
                    onChange={(e) => {
                      setSelectedDate(new Date(e.target.value));
                      setShowCalendar(false);
                    }}
                  />
                </div>
              )}
            </div>

            <div className="mt-12">
              <h1 className="text-6xl lg:text-8xl font-black uppercase tracking-tighter leading-[0.85] mb-6">
                {activeData.name.split(' ').slice(0, -1).join(' ')} <br />
                <span className={`text-transparent bg-clip-text bg-gradient-to-r ${activeData.color}`}>
                  {activeData.name.split(' ').pop()}
                </span>
              </h1>
              <div className="flex items-center justify-between gap-6">
                <p className="max-w-md text-zinc-400 text-xl font-medium leading-relaxed">
                  Insights for <span className="text-white">{activeData.name}</span> are live. Demand velocity is <span className="text-white font-bold">High</span>.
                </p>
                <button className="whitespace-nowrap bg-[#FF006E] text-white font-black uppercase px-10 py-5 rounded-full shadow-[0_10px_30px_rgba(255,0,110,0.4)] hover:scale-105 transition-all">
                  View Detail Report →
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* METRIC CARDS - Locked Grid */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-[#0c0c0e] border border-white/10 p-10 rounded-[40px] flex-1 flex flex-col justify-center shadow-xl">
            <p className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Viral Factor</p>
            <div className="flex items-baseline gap-2">
              <span className="text-8xl font-black tracking-tighter">{activeData.viral}</span>
              <span className="text-pink-500 text-3xl font-bold">/10</span>
            </div>
            <div className="h-2 bg-zinc-900 rounded-full mt-8 overflow-hidden">
              <div className="h-full bg-pink-500 shadow-[0_0_15px_#ec4899]" style={{ width: `${parseFloat(activeData.viral) * 10}%` }} />
            </div>
          </div>

          <div className="bg-[#0c0c0e] border-l-8 border-green-500 p-10 rounded-[40px] flex-1 flex flex-col justify-center shadow-xl">
            <p className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Predicted Revenue</p>
            <h3 className="text-7xl font-black tracking-tighter">+${activeData.revenue}</h3>
            <p className="text-green-500 font-black mt-4 uppercase tracking-tighter text-xs">1.2% Conversion Boost</p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default HeroSpotlight;