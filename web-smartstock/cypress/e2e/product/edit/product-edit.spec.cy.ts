import { faker } from '@faker-js/faker';

describe('Create Product Test', () => {
  beforeEach(() => {
    cy.login('admin.admin@sta.com', '123456');
    cy.navigateToProductEdit();
  });

  it('Show Edit Product Components', () => {
    cy.wait(1000);
    cy.contains('Editar Producto');
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
    cy.get('#discount_price').should('exist');
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
    cy.get('#product_name').click().clear();
    cy.get('#description').click().clear();
    cy.get('#unit_price').click().clear();
    cy.get('#url_photo').click().clear();
    cy.get('#store_conditions').click().clear();
    cy.get("#product_edit_title").click();

    cy.get('#product_name_required').should('exist');
    cy.get('#product_description_required').should('exist');
    cy.get('#product_unit_price_required').should('exist');
    cy.get('#product_url_photo_required').should('exist');
    cy.get('#product_store_conditions_required').should('exist');
    cy.get('.register-btn').should('exist').should('be.disabled');
  });

  it('Show Invalid Labels', () => {
    cy.wait(1000);
    cy.get('#product_name').clear().type(faker.lorem.words(50));
    cy.get('#description').clear().type(faker.lorem.words(50));
    cy.get('#product_name_exceed').should('exist');
    cy.get('#unit_price').clear().type(faker.datatype.number({ min: -1000, max: -1 }).toString());
    cy.get('#product_description_exceed').should('exist');
    cy.get('#is_promotion').check().check()
    //cy.get('#product_unit_price_invalid').should('exist');
    cy.get('#url_photo').clear().type(faker.lorem.word());
    cy.get("#product_edit_title").click();
    cy.get('#product_url_photo_invalid').should('exist');
  });

  it('Fill Edit Product Form Successfully', () => {
    cy.wait(1000);
    cy.get('#product_name').clear().type(faker.lorem.word());
    cy.get('#description').clear().type(faker.lorem.word());
    cy.get('#unit_price').clear().type(faker.datatype.number({ min: 1 }).toString());
    cy.get('#url_photo').clear().type(faker.image.imageUrl());
    cy.get('#store_conditions').clear().type(faker.lorem.words(10));
    cy.get('#currency').select(1);
    cy.get('#manufacturer').select(1);
    cy.get('#category').select(1);
    cy.get("#product_edit_title").click();
    cy.get('#expired_at').type(faker.date.future().toISOString().split('T')[0]);
    cy.get("#product_edit_title").click();
    cy.get('.register-btn').should('exist').should('not.be.disabled');
    cy.get('.register-btn').click();
    cy.contains('El producto fue editado con éxito.');
  });
});