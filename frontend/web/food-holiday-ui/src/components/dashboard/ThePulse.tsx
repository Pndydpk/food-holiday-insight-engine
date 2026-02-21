import React from 'react';

const ThePulse: React.FC = () => {
  return (
    <section className="px-10 py-16 bg-black text-white">
      {/* HEADER SECTION */}
      <div className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h2 className="text-4xl font-black uppercase tracking-tighter italic leading-none">
            The Pulse: <span className="text-zinc-600">Trending Holidays</span>
          </h2>
          <p className="text-zinc-500 mt-2 font-bold uppercase text-[11px] tracking-[0.3em]">
            Real-time Social Scraping & AI Modeling Active
          </p>
        </div>
        
        <div className="flex gap-3">
          {['Last 7 Days', 'All Holidays', 'Global'].map((filter) => (
            <button key={filter} className="px-5 py-2 bg-[#111113] border border-white/5 rounded-xl text-[10px] font-black uppercase tracking-widest hover:border-pink-500/50 transition-all">
              {filter} <span className="ml-2 text-zinc-600">▼</span>
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* TREND MONITORS (9 COLS) */}
        <div className="lg:col-span-9 grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* TIKTOK TRENDS CARD */}
          <div className="bg-[#0c0c0e] border border-white/5 rounded-[40px] p-8 relative group overflow-hidden shadow-2xl">
            <div className="flex justify-between items-start mb-10">
              <h4 className="text-xl font-black uppercase italic tracking-tighter">TikTok <br/><span className="text-zinc-500">Trends</span></h4>
              <div className="flex flex-col items-end">
                <span className="text-[10px] font-black text-pink-500 uppercase tracking-widest">Mentions</span>
                <div className="w-8 h-1 bg-pink-500 mt-1 shadow-[0_0_10px_#ec4899]" />
              </div>
            </div>
            
            {/* VIBRANT TREND LINE PLACEHOLDER */}
            <div className="h-40 w-full relative flex items-end">
              <svg className="w-full h-full" viewBox="0 0 100 40">
                <path 
                  d="M0 35 Q 20 35, 40 20 T 80 5 T 100 2" 
                  fill="none" 
                  stroke="#FF006E" 
                  strokeWidth="2.5"
                  className="drop-shadow-[0_0_8px_rgba(255,0,110,0.8)]"
                />
                {[0, 25, 50, 75, 100].map((x, i) => (
                   <circle key={i} cx={x} cy={35 - (i*6)} r="1.5" fill="#FF006E" />
                ))}
              </svg>
            </div>
            <div className="mt-4 flex justify-between text-[9px] font-black text-zinc-600 uppercase tracking-widest">
              <span>10 AM</span><span>2 PM</span><span>6 PM</span><span>10 PM</span>
            </div>
          </div>

          {/* INSTAGRAM TRENDS CARD */}
          <div className="bg-[#0c0c0e] border border-white/5 rounded-[40px] p-8 shadow-2xl">
            <div className="flex justify-between items-start mb-10">
              <h4 className="text-xl font-black uppercase italic tracking-tighter">Instagram <br/><span className="text-zinc-500">Trends</span></h4>
              <span className="text-[10px] font-black text-orange-500 uppercase tracking-widest">Mention</span>
            </div>
            <div className="h-40 w-full flex items-end gap-1.5">
               {[30, 45, 35, 60, 85, 70, 95].map((h, i) => (
                 <div key={i} className="flex-1 bg-gradient-to-t from-orange-500/20 to-orange-500 rounded-t-full shadow-[0_0_15px_rgba(249,115,22,0.3)]" style={{ height: `${h}%` }} />
               ))}
            </div>
            <div className="mt-4 flex justify-between text-[9px] font-black text-zinc-600 uppercase tracking-widest">
              <span>10 AM</span><span>2 PM</span><span>6 PM</span><span>10 PM</span>
            </div>
          </div>

          {/* ARTICLE TRENDS CARD */}
          <div className="bg-[#0c0c0e] border border-white/5 rounded-[40px] p-8 shadow-2xl">
            <div className="flex justify-between items-start mb-10">
              <h4 className="text-xl font-black uppercase italic tracking-tighter">Article <br/><span className="text-zinc-500">Trends</span></h4>
              <span className="text-[10px] font-black text-green-500 uppercase tracking-widest">Mentions</span>
            </div>
            <div className="h-40 flex items-end gap-2">
               {[20, 50, 30, 80, 40, 90, 100].map((h, i) => (
                 <div key={i} className="flex-1 bg-zinc-800 border-t-2 border-green-500/50" style={{ height: `${h}%` }} />
               ))}
            </div>
            <div className="mt-4 flex justify-between text-[9px] font-black text-zinc-600 uppercase tracking-widest">
              <span>Jan 1</span><span>Jan 2</span><span>Jan 3</span><span>Jan 4</span>
            </div>
          </div>

        </div>

        {/* TOP HOLIDAYS (3 COLS) */}
        <div className="lg:col-span-3 bg-[#0c0c0e] border border-white/10 rounded-[45px] p-10 flex flex-col shadow-2xl relative overflow-hidden">
          <div className="flex justify-between items-center mb-8">
            <h4 className="font-black uppercase italic text-sm tracking-tighter">Top Holidays</h4>
            <span className="text-zinc-600 text-[10px] font-black cursor-pointer hover:text-white transition-colors">SE STRATEGY ›</span>
          </div>

          {/* DONUT CHART COMPONENT */}
          <div className="relative w-52 h-52 mx-auto flex items-center justify-center">
            {/* Outer Glow Ring */}
            <div className="absolute inset-0 rounded-full border-[20px] border-zinc-900" />
            <div className="absolute inset-0 rounded-full border-[20px] border-[#FF006E] border-t-transparent border-l-transparent -rotate-45 shadow-[0_0_30px_rgba(255,0,110,0.3)]" />
            <div className="absolute inset-0 rounded-full border-[20px] border-cyan-400 border-b-transparent border-r-transparent rotate-[120deg]" />
            
            <div className="text-center z-10">
              <span className="block text-4xl font-black tracking-tighter">45%</span>
              <span className="text-[10px] text-zinc-500 uppercase font-black tracking-widest">Daily Share</span>
            </div>
          </div>

          {/* LEGEND TABLE */}
          <div className="mt-10 space-y-4">
            {[
              { name: 'Corn Chip Day', val: '45%', color: 'bg-[#FF006E]' },
              { name: 'Pizza Day', val: '33%', color: 'bg-cyan-400' },
              { name: 'Macaron Day', val: '12%', color: 'bg-purple-500' }
            ].map((item) => (
              <div key={item.name} className="flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <div className={`w-2.5 h-2.5 rounded-full ${item.color} shadow-[0_0_10px_currentColor]`} />
                  <span className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider">{item.name}</span>
                </div>
                <span className="text-[12px] font-black">{item.val}</span>
              </div>
            ))}
          </div>

          <div className="mt-auto pt-8 grid grid-cols-2 border-t border-white/5">
             <div className="border-r border-white/5 pr-4">
               <p className="text-[9px] font-black text-zinc-500 uppercase tracking-widest mb-1">Viral Comp</p>
               <p className="text-2xl font-black tracking-tighter">89%</p>
             </div>
             <div className="pl-6">
               <p className="text-[9px] font-black text-zinc-500 uppercase tracking-widest mb-1">Engage Rate</p>
               <p className="text-2xl font-black tracking-tighter">79%</p>
             </div>
          </div>
        </div>

      </div>
    </section>
  );
};

export default ThePulse;