/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "var(--brand-primary, #1e3a8a)",
          secondary: "var(--brand-secondary, #f59e0b)",
          bg: "var(--brand-bg, #ffffff)",
          text: "var(--brand-text, #111827)",
        },
      },
    },
  },
  plugins: [],
};
