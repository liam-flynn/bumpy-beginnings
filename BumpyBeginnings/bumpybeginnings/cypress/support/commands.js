// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// help from https://docs.cypress.io/app/end-to-end-testing/testing-your-app
Cypress.Commands.add('login', (username, password) => {
    cy.visit(`/login/`);

    cy.get('input[name="username"]').type(username);
    cy.get('input[name="password"]').type(`${password}{enter}`);

})

Cypress.Commands.add('loginAsStaff', () => {
    cy.visit(`/login/`);

    cy.get('input[name="username"]').type(Cypress.env('staff_username'));
    cy.get('input[name="password"]').type(`${Cypress.env('staff_password')}{enter}`);

})

