/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{html,js}"],
    theme: {
      extend: {
        colors: {
          primary: "#ff8500",
          'grey-color': "#606060"
        }
      },
    },
    plugins: [
        require('tailwind-scrollbar-hide')
  ],
}