/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{ts,tsx}", //ここを追加
  ],
  purge: {
    enabled: true,
    content: ['./src/pages/**/*.{js,ts,jsx,tsx}', './src/components/**/*.{js,ts,jsx,tsx}'], // ココ
  },
  darkMode: 'class', //ダークモードを有効化する
  theme: {
    extend: {
      colors: {
        darkgrey: '#222831', //darkModeで使用したい色を拡張定義
      },
    },
  },
  variants: {
    extend: {
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}; 