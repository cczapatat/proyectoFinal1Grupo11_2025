import { faker } from '@faker-js/faker';

describe('Assign Stock to Store', () => {
  it('Assign new stock to store', () => {
    cy.visit('/user-sessions/login');
    cy.get('#email').type('admin.admin@sta.com');
    cy.get('#password').type('123456');
    cy.get('#doLogin').click();
    cy.url().should('include', '/home')

    cy.get('.menu-toggle').click();
    cy.get('#nav_languages').click();
    cy.get('#nav_es-CO').click();
    cy.get('#nav_assign_products').click();

    cy.wait(2000);
    cy.url().should('include', '/assign-product');
  
    cy.contains('Carrefour');
    cy.contains('td', 'Carrefour') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 

    
    cy.contains('Chocoramo');
    cy.contains('td', 'Chocoramo')
    .parent('tr')
    .find('input[type="checkbox"]')
    .check()
    .click();

    cy.contains('td', 'Chocoramo')
    .parent('tr')
    .find('input[type="number"]')
    .clear()                              // clear the field
    .type('100');

    cy.wait(2000);
    //scroll down at the end of the page
    //cy.get('#saveBtt').scrollIntoView();

    cy.get('#saveBtt').should('not.be.disabled');
    cy.get('#saveBtt').click();
    cy.wait(200);
    
    cy.get('#saveBtt').should('be.disabled');

    cy.get('.menu-toggle').click()
    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
    
  });
});