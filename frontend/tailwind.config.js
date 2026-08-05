/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        gold: {
          light: '#B8860B',
          DEFAULT: '#DAA520',
          dark: '#FFD700',
        },
        parchment: {
          light: '#FFF8DC',
          DEFAULT: '#F5DEB3',
          dark: '#DEB887',
        },
        marble: '#F5F5F0',
        olympian: {
          light: '#2F6B5E',
          DEFAULT: '#3D8B7A',
          dark: '#4AA898',
        },
        charcoal: {
          light: '#2A2118',
          DEFAULT: '#1A1510',
          dark: '#0F0C08',
        }
      },
      fontFamily: {
        cinzel: ['Cinzel', 'serif'],
        crimson: ['Crimson Text', 'serif'],
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}