export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#05071a",
          900: "#0a0f2c",
          800: "#111838",
          700: "#1a2148",
          600: "#252d5c",
        },
        brand: {
          violet: "#8b5cf6",
          indigo: "#6366f1",
          blue: "#3b82f6",
          cyan: "#22d3ee",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "Segoe UI", "sans-serif"],
      },
      boxShadow: {
        card: "0 24px 60px -24px rgba(5, 7, 26, 0.85)",
        glow: "0 0 0 1px rgba(139, 92, 246, 0.35), 0 20px 45px -20px rgba(99, 102, 241, 0.55)",
      },
      backgroundImage: {
        "brand-gradient": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 55%, #22d3ee 100%)",
      },
      keyframes: {
        "fade-rise": {
          from: { opacity: "0", transform: "translateY(14px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
      animation: {
        "fade-rise": "fade-rise 0.45s ease-out both",
        float: "float 7s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
