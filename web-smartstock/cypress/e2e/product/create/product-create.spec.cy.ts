import { faker } from '@faker-js/faker';

describe('Create Product Test', () => {
  beforeEach(() => {
    cy.login('admin.admin@sta.com', '123456');
    cy.navigateToProductCreate();
  });

  it('Show Create Product Form Components', () => {
    cy.wait(1000);
    cy.contains('Crear Producto');
    cy.contains('Nombre');
    cy.get('#product_name').should('exist');
    cy.contains('Descripción');
    cy.get('#description').should('exist');
    cy.contains('Precio Unitario');
    cy.get('#unit_price').should('exist');
    cy.contains('Moneda');
    cy.get('#currency').should('exist');
    cy.contains('Categoría');
    cy.get('#category').should('exist');
    cy.contains('¿Es Promoción?');
    cy.get('#is_promotion').should('exist');
    cy.contains('Precio con Descuento');
    cy.get('#discount_price').should('exist').should('be.disabled');
    cy.contains('Fabricante');
    cy.get('#manufacturer').should('exist');
    cy.contains('Fecha de Vencimiento');
    cy.get('#expired_at').should('exist');
    cy.contains('Foto URL');
    cy.get('#url_photo').should('exist');
    cy.contains('Condiciones de Almacenamiento');
    cy.get('#store_conditions').should('exist');
  });

  it('Show Required Labels', () => {
    cy.wait(1000);
    cy.get('#product_name').click();
    cy.get('#description').click();
    cy.get('#unit_price').click();
    cy.get('#url_photo').click();
    cy.get('#store_conditions').click();
    cy.get("#product_create_title").click();

    cy.get('#product_name_required').should('exist');
    cy.get('#product_description_required').should('exist');
    cy.get('#product_unit_price_required').should('exist');
    cy.get('#product_url_photo_required').should('exist');
    cy.get('#product_store_conditions_required').should('exist');
    cy.get('.register-btn').should('exist').should('be.disabled');
  });

  it('Show Invalid Labels', () => {
    cy.wait(1000);
    cy.get('#product_name').type(faker.lorem.words(50));
    cy.get('#description').type(faker.lorem.words(50));
    cy.get('#product_name_exceed').should('exist');
    cy.get('#unit_price').type(faker.datatype.number({ min: -1000, max: -1 }).toString());
    cy.get('#product_description_exceed').should('exist');
    cy.get('#is_promotion').check().check()
    cy.get('#product_unit_price_invalid').should('exist');
    cy.get("#is_promotion").should('be.checked');
    cy.get('#discount_price').should('exist').should('not.be.disabled');
    cy.get('#discount_price').type(faker.datatype.number({ min: -1000, max: -1 }).toString());
    cy.get('#url_photo').type(faker.lorem.word());
    cy.get('#product_discount_price_invalid').should('exist');
    cy.get("#product_create_title").click();
    cy.get('#product_url_photo_invalid').should('exist');
  });

  it('Fill Create Product Form Successfully', () => {
    cy.wait(1000);
    cy.get('#product_name').type(faker.lorem.word());
    cy.get('#description').type(faker.lorem.word());
    cy.get('#unit_price').type(faker.datatype.number({ min: 1 }).toString());
    cy.get('#currency').select(1);
    cy.get('#manufacturer').select(1);
    cy.get('#category').select(1);
    cy.get('#is_promotion').check().should('be.checked');
    cy.get('#discount_price').should('exist').should('not.be.disabled');
    cy.get('#discount_price').type(faker.datatype.number({ min: 1 }).toString());
    cy.get('#url_photo').type(faker.image.imageUrl());
    cy.get('#store_conditions').type(faker.lorem.words(10));
    cy.get("#product_create_title").click();
    cy.get('.register-btn').should('exist').should('not.be.disabled');
    cy.get('.register-btn').click();
    cy.contains('El producto ha sido creado exitosamente');
  });
});