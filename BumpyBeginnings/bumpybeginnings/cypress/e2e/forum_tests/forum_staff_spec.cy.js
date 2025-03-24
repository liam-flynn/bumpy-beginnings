describe('Staff Forums Page', () => {
    // log in as a staff member before each test
    beforeEach(() => {
      cy.loginAsStaff();
      cy.visit('/forums/');
    });
  
    it('displays the "Create New Forum" button for staff members', () => {
      // the "Create New Forum" button should be visible only for staff users.
      cy.contains('Create New Forum').should('be.visible');
    });
  
    it('shows admin actions on each forum item', () => {
      // check that each forum list item contains admin action links.
      cy.get('.forum-list li').each(($li) => {
        cy.wrap($li).within(() => {
          // check for either a Deactivate or Reactivate button
          cy.get('a').then(($links) => {
            const hasDeactivate = $links.toArray().some(link => link.innerText.includes('Deactivate'));
            const hasReactivate = $links.toArray().some(link => link.innerText.includes('Reactivate'));
            expect(hasDeactivate || hasReactivate).to.be.true;
          });
          // also ensure the Delete button is present.
          cy.contains('Delete').should('exist');
        });
      });
    });
  
    it('allows staff to create and then delete a forum', () => {
        // generate a unique forum name.
        const uniqueForumName = `Test Forum ${Date.now()}`;
        
        // visit the forum creation page
        cy.visit('/forums/new/');
      
        // fill in the forum creation form
        cy.get('input[name="forumName"]').type(uniqueForumName);
        cy.get('textarea[name="description"]').type('This forum is created for testing deletion.');
      
        // submit the form
        cy.get('form').submit();
      
        // confirm that we are redirected to the forums list page
        cy.url().should('include', '/forums/');
      
        // ensure the newly created forum appears in the forum list
        cy.contains('.forum-list li', uniqueForumName).should('be.visible');
      
        // find the forum item and perform deletion
        cy.contains('.forum-list li', uniqueForumName).then(($forumItem) => {
          // within this forum item, stub the confirm dialog to automatically accept deletion
          cy.wrap($forumItem).within(() => {
            cy.on('window:confirm', () => true);
            // click the Delete link
            cy.contains('Delete').click();
          });
        });
      
        // verify that the forum is no longer visible on the page after deletion
        cy.contains(uniqueForumName).should('not.exist');
      });
  });