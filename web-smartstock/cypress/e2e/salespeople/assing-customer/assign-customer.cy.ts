import { faker } from '@faker-js/faker';

describe('Associale Seller to clients Test', () => {
  it('Associate Sellers', () => {
    cy.visit('/user-sessions/login');
    cy.get('#email').type('admin.admin@sta.com');
    cy.get('#password').type('123456');
    cy.get('#doLogin').click();
    cy.url().should('include', '/home')

    cy.get('.menu-toggle').click();
    cy.get('#nav_languages').click();
    cy.get('#nav_es-CO').click();
    cy.get('#nav_assign_customers').click();

  
    cy.contains('jhon1@sta.com');
    cy.contains('td', 'jhon1@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 


    cy.contains('aclientcypress@sta.com');
    cy.contains('td', 'aclientcypress@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 

    cy.contains('aclientcypress1@sta.com');
    cy.contains('td', 'aclientcypress1@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 

    cy.contains('aclientcypress2@sta.com');
    cy.contains('td', 'aclientcypress2@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 
    
    cy.contains('aclientcypress3@sta.com');
    cy.contains('td', 'aclientcypress3@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 


    cy.get('#associate-save').click();  //save


    cy.contains('seller@sta.com');
    cy.contains('td', 'seller@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 

    cy.contains('jhon1@sta.com');
    cy.contains('td', 'jhon1@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .check(); 


    cy.contains('td', 'aclientcypress@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .should('be.checked'); 

    cy.contains('td', 'aclientcypress1@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .should('be.checked'); 

    cy.contains('td', 'aclientcypress2@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .should('be.checked'); 

    cy.contains('td', 'aclientcypress3@sta.com') // find the cell with the target email
    .parent('tr')                         // go to the parent row
    .find('input[type="checkbox"]')      // find the checkbox in that row
    .should('be.checked'); 


    cy.get('.menu-toggle').click()
    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
    
  });
});