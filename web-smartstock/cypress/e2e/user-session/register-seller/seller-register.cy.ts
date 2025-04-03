import { faker } from '@faker-js/faker';

describe('Create A Seller Test', () => {
  it('Create New Seller', () => {
    cy.visit('/user-sessions/login');
    cy.get('#email').type('admin.admin@sta.com');
    cy.get('#password').type('123456');
    cy.get('#doLogin').click();
    cy.url().should('include', '/home')

    cy.get('.menu-toggle').click();
    cy.get('#nav_languages').click();
    cy.get('#nav_es-CO').click();
    cy.get('#nav_sellers').click();

    cy.get('#name').type('Test Seller');
    cy.get('#phone').type(faker.phone.number('+###########'));
    cy.get('#email').type(`${faker.internet.userName()}@${faker.internet.domainName()}`);
    cy.get('#password').type('123456');
    cy.get('#confirmPassword').type('123456');
    cy.get('#zone').select('NORTH');
    cy.get('#quotaExpected').type('200000');
    cy.get('#currencyQuota').select('USD');
    cy.get('#quarterlyTarget').type('20000');
    cy.get('#currencyTarget').select('USD');
    cy.get('#performanceRecomendations').type('Be the best seller ever');
    cy.get('#seller_btn_create').click();

    
    cy.contains('Vendedor creado exitosamente');

    cy.get('.menu-toggle').click()
    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
  });
});