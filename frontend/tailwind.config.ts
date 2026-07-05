import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        sand: "#f4ece2",
        taupe: "#b39272",
        espresso: "#2e2018",
        rosewood: "#9c5f50",
        moss: "#64735f"
      },
      boxShadow: {
        card: "0 30px 80px rgba(46, 32, 24, 0.08)"
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        sans: ["DM Sans", "sans-serif"]
      },
      backgroundImage: {
        haze: "radial-gradient(circle at top left, rgba(243, 217, 195, 0.9), transparent 35%), radial-gradient(circle at 90% 10%, rgba(214, 201, 176, 0.7), transparent 30%), linear-gradient(180deg, #fcfaf7 0%, #f0e6db 100%)"
      }
    }
  },
  plugins: []
} satisfies Config;

