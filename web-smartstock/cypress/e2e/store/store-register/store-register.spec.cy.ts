import { faker } from '@faker-js/faker';

describe('Create Store Test', () => {
  it('Create Store', () => {
    cy.visit('/user-sessions/login');
    cy.get('#email').type('admin.admin@sta.com');
    cy.get('#password').type('123456');
    cy.get('#doLogin').click();
    cy.url().should('include', '/home')

    cy.get('.menu-toggle').click();
    cy.get('#nav_languages').click();
    cy.get('#nav_es-CO').click();
    cy.get('#nav_store_register').click();

    cy.get('#store_name').type('Test Store');
    cy.get('#store_phone').type(faker.phone.number('###########'));
    cy.get('#store_email').type(`${faker.internet.userName()}@${faker.internet.domainName()}`);
    cy.get('#store_address').type('Test Address');
    cy.get('#store_capacity').type('100');
    cy.get('#store_state').select('ACTIVE');
    cy.get('#store_security_level').select('HIGH');
    cy.get('#store_btn_register').click();

    cy.contains('Registro Exitoso');
    cy.contains('La bodega ha sido creada exitosamente.');

    cy.get('.menu-toggle').click()
    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
  });
});