import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Editorial paper canvas
        paper: "#f8f3ea",
        parchment: "#fbf8f2",
        // Warm neutrals
        sand: "#f1e7d9",
        taupe: "#b39272",
        // Ink / text
        ink: "#211a14",
        espresso: "#2a1f17",
        // Accents
        rosewood: "#8f4e3f",
        gold: "#b08d57",
        champagne: "#d8c3a0",
        moss: "#64735f",
        blush: "#e8d5cc",
        // Hairline rules
        line: "#e2d6c4"
      },
      boxShadow: {
        card: "0 30px 80px rgba(42, 31, 23, 0.07)",
        editorial: "0 1px 0 rgba(42, 31, 23, 0.04), 0 24px 60px -30px rgba(42, 31, 23, 0.28)",
        lift: "0 40px 90px -40px rgba(42, 31, 23, 0.4)"
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        sans: ["DM Sans", "sans-serif"]
      },
      letterSpacing: {
        masthead: "0.42em"
      },
      backgroundImage: {
        haze: "radial-gradient(circle at top left, rgba(243, 217, 195, 0.9), transparent 35%), radial-gradient(circle at 90% 10%, rgba(214, 201, 176, 0.7), transparent 30%), linear-gradient(180deg, #fcfaf7 0%, #f0e6db 100%)"
      }
    }
  },
  plugins: []
} satisfies Config;
