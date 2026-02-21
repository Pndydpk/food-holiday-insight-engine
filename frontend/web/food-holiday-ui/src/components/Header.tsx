import React, { useState, useEffect } from 'react';
import logo from '../assets/logo_without_bg_without_text_glow.png';

const Header: React.FC = () => {
  const [timeData, setTimeData] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const formatted = now.toLocaleString('en-US', {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      }).toUpperCase();

      setTimeData(formatted);
    };

    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="flex items-center justify-between px-10 py-5 bg-[#030303] border-b border-white/5 sticky top-0 z-50">
      {/* Brand Section */}
      <div className="flex items-center gap-4">
        <img 
          src={logo} 
          alt="FoodLens Logo" 
          className="w-12 h-12 object-contain drop-shadow-[0_0_8px_rgba(34,197,94,0.3)]" 
        />
        
        <span 
          className="text-[28px] font-black tracking-tighter text-white uppercase"
          style={{
            textShadow: `
              0 0 10px rgba(255, 120, 50, 1),
              0 0 20px rgba(255, 100, 50, 0.8),
              0 0 40px rgba(255, 50, 50, 0.4)
            `
          }}
        >
          FOODLENS
        </span>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-8">
        <div className="hidden lg:block">
          <span className="text-[11px] font-bold text-zinc-500 tracking-[0.2em] font-mono">
            {timeData}
          </span>
        </div>
        
        {/* Refined Elliptical/Oval Button */}
        <button className="
          px-8 py-2.5 
          border-[1.5px] border-[#FF006E] 
          bg-transparent hover:bg-[#FF006E] 
          text-white text-[12px] font-black uppercase tracking-widest 
          rounded-full 
          transition-all duration-300 ease-in-out
          hover:shadow-[0_0_25px_rgba(255,0,110,0.7)]
          active:scale-95
        ">
          Contact Us
        </button>
      </div>
    </header>
  );
};

export default Header;