/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ethiopia: {
          green: "#078930",
          yellow: "#FCDD09",
          red: "#DA121A",
          blue: "#0F47AF"
        },
        hazard: {
          low: "#10b981",
          moderate: "#f59e0b",
          high: "#f97316",
          critical: "#dc2626"
        }
      }
    }
  },
  plugins: []
}
