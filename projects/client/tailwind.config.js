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
        "c60-bg": "#222831",
        "c60-fg": "#EEEEEE",

        "c30-bg": "#31363F",
        "c30-fg": "#EEEEEE",

        "c10-bg": "#EEEEEE",
        "c10-fg": "#76ABAE",

        "c10-bg-active": "#7fabad",
        "c10-fg-active": "#FFFFFF",

        "c-fg-disabled": "#EEEEEE",
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
