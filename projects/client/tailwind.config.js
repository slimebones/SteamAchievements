/** @type {import('tailwindcss').Config} */

const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./src/**/*.{html,ts,js}",
  ],
  theme: {
    extend: {
      // fg => foreground
      // bg => background
      colors: {
        "c60-bg": "#070F2B",
        "c60-fg": "#FFFFFF",

        "c30-bg": "#1B1A55",
        "c30-fg": "#FFFFFF",

        "c10-fg": "#FFFFFF",
        "c10-bg": "#535C91",

        "c10-bg-active": "#9290C3",
        "c10-fg-active": "#FFFFFF",

        "c-fg-disabled": "#FFFFFF",
        "c-bg-disabled": colors.gray["300"]
      },
      animation: {
        "spin-slow": "spin 3s linear infinite",
        "wiggle": "wiggle 1s ease-in-out infinite"
      },
      keyframes: {
        wiggle: {
          "0%, 100%": { transform: "rotate(-3deg)" },
          "50%": { transform: "rotate(3deg)" },
        }
      }
    },
  },
  plugins: [
  ],
};
