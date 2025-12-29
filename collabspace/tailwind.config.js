/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#e6e8ef",
        inkMuted: "#ffffff",
        bg: "#0c0d11",
        bgElevated: "#11131a",
        border: "#1c1f27",
        accent: {
          blue: "#4da3ff",
          link: "#69b3ff",
        },
        surface: "#0f1117",
        success: "#22c55e",
        warning: "#fbbf24",
        danger: "#ef4444",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
      },
      borderRadius: {
        card: "14px",
        btn: "10px",
      },
      boxShadow: {
        card: "0 16px 38px rgba(0,0,0,0.3)",
        glow: "0 0 18px rgba(77,163,255,0.25)",
        inset: "inset 0 1px 0 rgba(255,255,255,0.04)",
      },
    },
  },
  plugins: [],
};