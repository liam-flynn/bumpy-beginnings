describe("Forum Tests", () => {
  beforeEach(() => {
    cy.login(Cypress.env("user_username"), Cypress.env("user_password"));
  });

  it("Should display the list of forums", () => {
    cy.visit("/forums/");
    cy.contains("Forums").should("be.visible");
    // ensure there's at least one forum item in the list
    cy.get(".forum-list > li").should("have.length.greaterThan", 0);
  });

  it("Should navigate to a forum's detail page", () => {
    cy.visit("/forums/");
    // click the first forum to go into it
    cy.get(".forum-list li a").first().click();
    // verify the URL now contains a forum id (e.g. /forums/1/)
    cy.url().should("match", /\/forums\/\d+\//);
    cy.contains("Posts").should("be.visible");
  });

  it("Should allow creating a new post", () => {
    cy.visit("/forums/1/");

    // fill in the post title
    cy.get("input[name='postTitle']").type("Test Post Title");

    // wait for the TinyMCE iframe to load.
    cy.get("iframe.tox-edit-area__iframe", { timeout: 10000 })
      .should("be.visible")
      // type into iframe
      // help from https://www.lambdatest.com/blog/how-to-handle-iframes-in-cypress/
      .then(($iframe) => {
        const $body = $iframe.contents().find("body");
        cy.wrap($body).clear().type("This is a test post.");
      });

    // submit the form
    cy.contains("Submit").click();

    // verify that the new post appears on the page
    cy.contains("Test Post Title").should("be.visible");
  });

  it("Should allow deleting a post if authorized", () => {
    cy.visit("/forums/1/");
    cy.get("button:contains('Delete')").first().click();
    cy.on("window:confirm", () => true);
    cy.contains("Test Post Title").should("not.exist");
  });

  it("Should allow adding a comment and then deleting it", () => {
    cy.visit("/forums/1/posts/1/");

    // fill in the TinyMCE editor for the comment
    cy.get("iframe#id_commentText_ifr", { timeout: 10000 })
      .should("be.visible")
      .then(($iframe) => {
        const $body = $iframe.contents().find("body");
        cy.wrap($body).clear().type("This is a test comment.");
      });

    // submit the comment
    cy.contains("Submit").click();

    // wait for the new comment to appear
    cy.contains("This is a test comment.", { timeout: 10000 }).should(
      "be.visible"
    );

    // delete the comment so it doesn't accumulate on the forum page.
    cy.contains(".comments > li", "This is a test comment.", {
      timeout: 10000,
    }).within(() => {
      // automatically confirm the delete confirmation
      cy.on("window:confirm", () => true);
      cy.contains("Delete").click();
    });

    // verify that the comment has been removed from the page
    cy.contains("This is a test comment.", { timeout: 10000 }).should(
      "not.exist"
    );
  });

  it("Should allow upvoting and downvoting comments", () => {
    cy.visit("/forums/1/posts/1/");

    // filter through the comment list items to find one that has both upvote and downvote buttons and a score of 0.
    cy.get("ul.space-y-6 > li")
      .filter((index, el) => {
        const $el = Cypress.$(el);
        const upvoteBtn = $el.find("button[id^='upvote-btn-']");
        const downvoteBtn = $el.find("button[id^='downvote-btn-']");
        const scoreText = $el.find("span[id^='score-']").text().trim();
        return (
          upvoteBtn.length > 0 && downvoteBtn.length > 0 && scoreText === "0"
        );
      })
      .first()
      .then(($comment) => {
        // extract the comment ID from the upvote button's ID
        const upvoteId = $comment.find("button[id^='upvote-btn-']").attr("id");
        const commentId = upvoteId.split("upvote-btn-")[1];

        // upvote the comment and verify the score increments to 1
        cy.get(`#upvote-btn-${commentId}`).click();
        cy.get(`#score-${commentId}`, { timeout: 10000 }).should(
          "contain",
          "1"
        );

        // downvote the comment and verify the score returns to 0
        cy.get(`#downvote-btn-${commentId}`).click();
        cy.get(`#score-${commentId}`, { timeout: 10000 }).should(
          "contain",
          "-1"
        );
        // set it back to what it was
        cy.get(`#downvote-btn-${commentId}`).click();
      });
  });
});
