describe("Login Tests", () => {

    beforeEach(() => {
      cy.visit(`/login/`);
    });
  
    it("Should display the login form", () => {
      cy.contains("Sign In").should("be.visible");
      cy.get("form#login_form").should("be.visible");
    });
  
    it("Should log in successfully with valid credentials", () => {
      cy.get('input[name="username"]').type(Cypress.env('user_username'));
      cy.get('input[name="password"]').type(Cypress.env('user_password'));
      cy.get("form#login_form").submit();
  
      // Verify successful login
      cy.url().should("eq", `${Cypress.config("baseUrl")}/`);
      cy.contains("Logout").should("be.visible"); 
    });
  
    it("Should show an error for invalid credentials", () => {
      cy.get('input[name="username"]').type("invaliduser");
      cy.get('input[name="password"]').type("invalidpassword");
      cy.get("form#login_form").submit();
  
      // Verify error message
      cy.contains("Invalid login").should("be.visible");
      cy.url().should("eq", `${Cypress.config("baseUrl")}/login/`);
    });
  
    it("Should show validation errors for empty fields", () => {
      cy.get("form#login_form").submit();
  
      cy.contains('Username is required').should('be.visible');
      cy.contains('Password is required').should('be.visible');
      cy.url().should("eq", `${Cypress.config("baseUrl")}/login/`); 
    });
  
    it("Should navigate to the registration page", () => {
      cy.contains("Register here").click();
  
      // Verify redirection to the registration page
      cy.url().should("eq", `${Cypress.config("baseUrl")}/register/`);
      cy.contains("Register").should("be.visible");
    });
  });