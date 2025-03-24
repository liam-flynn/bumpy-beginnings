const { defineConfig } = require("cypress");

module.exports = defineConfig({
  viewportWidth: 1920,
  viewportHeight: 1080,
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    baseUrl: "https://localhost:8000",
  },
  env: {
    user_username: '',
    user_password: '',
    staff_username: '',
    staff_password: ''
  }
});
