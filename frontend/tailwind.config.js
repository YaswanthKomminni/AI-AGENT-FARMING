/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        farm: {
          green: '#16a34a',
          lightgreen: '#bbf7d0',
          earth: '#92400e',
          sky: '#0369a1',
          gold: '#d97706',
          cream: '#fefce8',
        },
      },
    },
  },
  plugins: [],
}
