import { faker } from '@faker-js/faker';

describe('Create Massive Products Test', () => {
  beforeEach(() => {
    cy.login('admin.admin@sta.com', '123456');
    cy.navigateToMassiveProductsCreate();
  });

  it('Show Create Massive Products Form Components', () => {
    cy.wait(1000);
    cy.contains('Registro Masivo de Productos');
    cy.get('#upload-icon').should('exist');
    cy.contains('Selecciona el archivo que deseas subir desde tu computador.');
    cy.get('#upload_btn').should('exist');
    cy.contains('Hasta 300 MB para archivos CSV');
  });

  it('Upload CSV File Success', () => {
    const fileName = 'products.csv';
    cy.get('#file_input').attachFile(fileName);
    cy.get('#file_info').should('contain', fileName);
    cy.get('#proccess_btn').should('exist');
    cy.get('#proccess_btn').should('not.be.disabled');
    cy.get('#proccess_btn').click();
    cy.get('#upload-icon').should('exist');
    cy.get('#uploaded_description').should('contain', fileName);
    cy.get('#file_uploaded_notification').should('exist');
    cy.get('#file_size_error').should('not.exist');
    cy.contains('El archivo se ha cargado exitosamente.');
  });

  it('Upload CSV File Error', () => {
    const fileName = 'bad_file.txt';
    cy.get('#file_input').attachFile(fileName);
    cy.get('#file_info').should('contain', fileName);
    cy.get('#proccess_btn').should('exist');
    cy.get('#proccess_btn').should('not.be.disabled');
    cy.get('#proccess_btn').click();
    cy.get('#file_uploaded_notification').should('not.exist');
    cy.contains('El archivo no puede ser cargado.');
  });
});