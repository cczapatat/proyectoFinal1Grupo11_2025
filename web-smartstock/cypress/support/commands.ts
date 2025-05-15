// ***********************************************
// This example namespace declaration will help
// with Intellisense and code completion in your
// IDE or Text Editor.
// ***********************************************
// declare namespace Cypress {
//   interface Chainable<Subject = any> {
//     customCommand(param: any): typeof customCommand;
//   }
// }
//
// function customCommand(param: any): void {
//   console.warn(param);
// }
//
// NOTE: You can use it like so:
// Cypress.Commands.add('customCommand', customCommand);
//
// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('login', (email, password) => {
  cy.visit('/user-sessions/login');
  cy.get('#email').type(email);
  cy.get('#password').type(password);
  cy.get('#doLogin').click();
  cy.url().should('include', '/home');
});

Cypress.Commands.add('logout', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_btn_logout').click();
  cy.url().should('include', '/user-sessions/login');
});

Cypress.Commands.add('navigateToProductCreate', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_products').click();
  cy.get('#nav_products_register').click();
  cy.url().should('include', '/product/create');
});

Cypress.Commands.add('navigateToProductEdit', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_products').click();
  cy.get('#nav_products_modify').click();
  cy.url().should('include', '/product/list');
  cy.get('#product_list_table tbody tr')
    .first()
    .find('button')
    .click();
});

Cypress.Commands.add('navigateToCreateOrder', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_languages').click();
  cy.get('#nav_es-CO').click();
  cy.get('#nav_create_order').click();
  cy.url().should('include', '/order/create');
});

Cypress.Commands.add('navigateToMassiveProductsCreate', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_massive').click();
  cy.get('#nav_massive_products_create').click();
  cy.url().should('include', '/massive/product/create');
});

Cypress.Commands.add('navigateToMassiveManufacturersCreate', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_massive').click();
  cy.get('#nav_massive_manufactures').click();
  cy.url().should('include', '/massive/manufacture');
});

Cypress.Commands.add('navigateToMassiveProductsEdit', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_massive').click();
  cy.get('#nav_massive_products_modify').click();
  cy.url().should('include', '/massive/product/edit');
});

Cypress.Commands.add('navigateToManufactureListProducts', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_languages').click();
  cy.get('#nav_es-CO').click();
  cy.get('#nav_customers').click();
  cy.get('#nav_customer_search').click();
  cy.url().should('include', '/manufacturers/list-products');
});

Cypress.Commands.add('navigateToAlarmCreate', () => {
  cy.get('.menu-toggle').click();
  cy.get('#nav_alarm_create').click();
  cy.url().should('include', '/alarm/create');
});
