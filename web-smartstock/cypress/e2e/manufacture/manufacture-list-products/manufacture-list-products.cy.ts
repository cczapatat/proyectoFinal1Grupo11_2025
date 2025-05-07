describe('Manufacture List Products Test', () => {
  beforeEach(() => {
    cy.login('admin.admin@sta.com', '123456');
    cy.navigateToManufactureListProducts();
  });

  afterEach(() => {
    cy.logout();
  });

  it('Manufacture List Products', () => {
    cy.wait(1000);
    cy.contains('Productos');
    cy.contains('Fabricantes');
    cy.contains('Lista productos de un Fabricante');

    cy.get('#manufacturersTable').should('exist');
    cy.get('#manufacturersTable tbody tr').should('have.length', 10);
    cy.get('#manufacturersTable tbody tr input[type="checkbox"]').should('have.length.greaterThan', 1);
    cy.get('#manufacturersTable tbody tr').first().find('td').should('have.length', 4);
    cy.get('#manufacturersTable tbody tr').first().find('td input[type="checkbox"]').first().click();
    cy.wait(500);

    cy.get('#productsTable').should('exist');
    cy.get('#productsTable tbody tr').should('have.length', 10);
    cy.get('#productsTable tbody tr').first().find('td').should('have.length', 3);
    cy.get('#productsTable tbody tr').first().find('td input[type="checkbox"]').first().should('be.checked');
    cy.get('#products-btn-pages').should('exist');
    cy.wait(500);

    cy.get('#manufacturersTable tbody tr').first().find('td input[type="checkbox"]').first().click();
    cy.get('#productsTable').should('exist');
    cy.get('#productsTable tbody tr').should('have.length', 10);
    cy.get('#products-btn-pages').should('not.exist');
    cy.contains('Seleccionar un Fabricante');
  });
});
