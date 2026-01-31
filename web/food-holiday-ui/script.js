function updateClock() {
    const now = new Date();
    const options = { 
        weekday: 'long', year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true 
    };
    document.getElementById('live-clock').textContent = now.toLocaleString(undefined, options).toUpperCase();
}

const foodHolidays = {
    "Jan 29": { name: "NATIONAL CORN CHIP DAY", factor: "9.4", revenue: "+$12.4k" },
    "Jan 30": { name: "NATIONAL CROISSANT DAY", factor: "8.5", revenue: "+$8.2k" }
};

function updateHoliday() {
    const now = new Date();
    const dateKey = now.toLocaleString('en-US', { month: 'short', day: '2-digit' });
    const today = foodHolidays[dateKey] || { name: "GLOBAL FOOD DAY", factor: "5.0", revenue: "+$2.0k" };

    document.getElementById('hero-title').innerHTML = today.name.replace(" ", "<br>");
    document.getElementById('viral-val').textContent = today.factor + "/10";
    document.getElementById('revenue-val').textContent = today.revenue;
    document.getElementById('hero-month').textContent = dateKey.split(" ")[0].toUpperCase();
    document.getElementById('hero-day').textContent = dateKey.split(" ")[1];
}

setInterval(updateClock, 1000);
updateClock();
updateHoliday();