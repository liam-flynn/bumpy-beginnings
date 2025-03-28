describe('Eligibility Questionnaire', () => {
  
  beforeEach(() => {
    cy.login(Cypress.env("user_username"), Cypress.env("user_password"));
      // visit the questionnaire page.
      cy.visit('/calculator/');
    });
  
    it('displays an error when residency is false', () => {
      // verify the questionnaire page is loaded.
      cy.contains('Eligibility Questionnaire').should('be.visible');
  
      // say no to uk residency
      cy.get('input[name="residency"][value="false"]').check();
  
      // fill the salary field.
      cy.get('input[name="salary"]').type('25000');
  
      // submit the form.
      cy.get('form').submit();
  
      // verify that the error message is displayed on the results page.
      cy.contains("Unfortunately, you must live in the UK to qualify for any benefits.")
        .should('be.visible');
    });
  
    it('processes a valid submission when residency is true', () => {
      // verify the questionnaire page is loaded.
      cy.contains('Eligibility Questionnaire').should('be.visible');
  
      // say you are a uk resident
      cy.get('input[name="residency"][value="true"]').check();
  
      // fill in the salary field.
      cy.get('input[name="salary"]').type('16000');
  
      // for each criterion, if it is a boolean question, select "Yes".
      cy.get('form').within(() => {
        cy.get('input[name^="criterion_"][type="radio"][value="true"]').each(($radio) => {
          // check each "Yes" radio button for criteria.
          cy.wrap($radio).check({ force: true });
        });
      });
  
      // submit the form.
      cy.get('form').submit();
  
      // confirm that the error message is not displayed.
      cy.contains("Unfortunately, you must live in the UK").should('not.exist');
  
      // check that some results have appeared.
      cy.contains('following benefits have been identified').should('exist');
    });
  });