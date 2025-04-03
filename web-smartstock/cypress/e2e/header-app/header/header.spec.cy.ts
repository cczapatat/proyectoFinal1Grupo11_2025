describe('Header App Test', () => {
  it('Header App', () => {
    cy.visit('/user-sessions/login');
    cy.get('#email').type('admin.admin@sta.com');
    cy.get('#password').type('123456');
    cy.get('.btn-info').click();
    cy.contains('Login successful as ADMIN');

    cy.get('.menu-toggle').click();
    cy.get('#nav_languages').click();

    cy.get('#nav_es-CO').click();
    cy.get('#nav_store_register').should('contain.text', 'Bodegas');

    cy.get('#nav_es-AR').click();
    cy.get('#nav_store_register').should('contain.text', 'Almacenes');

    cy.get('#nav_en-UK').click();
    cy.get('#nav_store_register').should('contain.text', 'Stores');

    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
  });
});