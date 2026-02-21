/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Tailwind scans these for classes
  ],
  theme: {
    extend: {
      colors: {
        'foodlens-dark': '#0a0a0a',
        'foodlens-neon': '#39FF14', // Example neon green
      }
    },
  },
  plugins: [],
}