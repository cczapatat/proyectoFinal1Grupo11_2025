import { faker } from '@faker-js/faker';

describe('Create Product Test', () => {
  beforeEach(() => {
    cy.login('admin.admin@sta.com', '123456');
    cy.navigateToAlarmCreate();
  });

  it('Show Create Product Form Components', () => {
    cy.wait(1000);
    cy.contains('Crear Alarma');
    cy.contains('Fabricante');
    cy.get('#manufacture_id').should('exist');
    cy.contains('Producto');
    cy.get('#product_id').should('exist');
    cy.contains('Valor Mínimo');
    cy.get('#minimum_value').should('exist');
    cy.contains('Valor Máximo');
    cy.get('#maximum_value').should('exist');
    cy.contains('Notas');
    cy.get('#notes').should('exist');
  });

  it('Show Required Labels', () => {
    cy.wait(1000);
    cy.get('#is_set_min_value').click();
    cy.get('#minimum_value').click();
    cy.get("#alarm_create_title").click();
    cy.get('#is_set_max_value').click();
    cy.get('#maximum_value').click();
    cy.get('#notes').click();
    cy.get("#alarm_create_title").click();

    cy.get('#alarm_min_value_required').should('exist');
    cy.get('#alarm_max_value_required').should('exist');
    cy.get('#alarm_notes_required').should('exist');
    cy.get('.register-btn').should('exist').should('be.disabled');
  });

  it('Show Invalid Labels', () => {
    cy.wait(1000);
    cy.get('#is_set_min_value').click();
    cy.get('#minimum_value').type("-100");
    cy.get('#is_set_max_value').click();
    cy.get('#maximum_value').type("-100");
    cy.get('#notes').click();
    cy.get('#alarm_min_value_invalid').should('exist');
    cy.get('#alarm_max_value_invalid').should('exist');
    cy.get('.register-btn').should('exist').should('be.disabled');
  });

  it('Fill Create Alarm Form Successfully', () => {
    cy.wait(1000);
    cy.get('#manufacture_id').select(1);
    cy.get('#product_id').select(1);
    cy.get('#is_set_min_value').click();
    cy.get('#minimum_value').type("1");
    cy.get('#is_set_max_value').click();
    cy.get('#maximum_value').type("10");
    cy.get('#notes').type(faker.lorem.word());
    cy.get("#alarm_create_title").click();
    cy.get('.register-btn').should('exist').should('not.be.disabled');
    cy.get('.register-btn').click();
    cy.contains('La alarma ha sido creada exitosamente');
  });
});