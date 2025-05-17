describe('List Seller´s clients Test', () => {
  it('Create New Seller', () => {
    cy.visit('/user-sessions/login');
    cy.get('#email').type('admin.admin@sta.com');
    cy.get('#password').type('123456');
    cy.get('#doLogin').click();
    cy.url().should('include', '/home')

    cy.get('.menu-toggle').click();
    cy.get('#nav_languages').click();
    cy.get('#nav_es-CO').click();
    cy.get('#nav_customers').click();
    cy.get('#nav_customer_list').click();
  
    cy.contains('acypress2@sta.com');
    cy.contains('td', 'acypress2@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 

    cy.contains('client@client.com');

    
    cy.contains('mzaidiro.mendoza8@sta.com');
    cy.contains('td', 'mzaidiro.mendoza8@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 


    cy.get('#empty-customer').should('be.visible');

    cy.get('.menu-toggle').click()
    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
    
  });
});