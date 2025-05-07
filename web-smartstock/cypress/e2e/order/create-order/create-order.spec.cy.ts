describe('Create Order Test', () => {
  afterEach(() => {
    cy.logout();
  });

  it('Create Order As Admin', () => {
    cy.login('admin.admin@sta.com', '123456');
    cy.navigateToCreateOrder();

    cy.wait(1000);
    cy.contains('Crear Order');
    cy.contains('Vendedor');
    cy.get('#order_created_seller').should('exist');
    cy.contains('Cliente');
    cy.get('#order_created_client').should('exist');
    cy.contains('Fecha de Entrega');
    cy.get('#order_created_delivery_date').should('exist');
    cy.contains('Productos');
    cy.get('#order_created_products_label').should('exist');
    cy.get('#btn_open_product_stocks').should('exist');
    cy.contains('Método de Pago');
    cy.get('#paymentMethod_CREDIT_CARD').should('exist');
    cy.contains('Total');
    cy.get('#order_create_total_amount').contains('0');
    cy.get('#order_create_total_amount').should('exist');
    cy.contains('Crear');
    cy.get('#btn_create_order').should('exist').should('be.disabled');

    cy.get('#order_created_seller').select('seller (seller@seller.com)');
    cy.wait(1000);

    cy.get('#order_created_client').select('client (client@client.com)');
    cy.wait(500);

    cy.get('#btn_open_product_stocks').click();
    cy.get('#btn_create_order_previous_stock_page').should('exist');
    cy.get('#btn_create_order_next_stock_page').should('exist');
    cy.get('#create_order_checkbox_0').should('exist')
      .check()
      .should('be.checked');
    cy.wait(200);
    cy.get('#create_order_btn_increase_0').should('exist').should('not.be.disabled');
    cy.get('#create_order_btn_decrease_0').should('exist').should('be.disabled');
    cy.get('#create_order_btn_increase_0').click().click();
    cy.get('#create_order_btn_decrease_0').should('not.be.disabled').click();
    cy.get('#btn_create_order_add_products').should('exist').click();

    cy.get('#order_created_product_selected_0').should('exist');
    cy.get('#order_create_total_amount').should('not.contain', '0');
    cy.get('#create_order_btn_increase_quantity_0').should('exist').should('not.be.disabled').click();
    cy.get('#create_order_btn_decrease_quantity_0').should('exist').should('not.be.disabled').click().click();
    cy.get('#create_order_btn_decrease_quantity_0').should('exist').should('be.disabled');

    cy.get('#paymentMethod_CREDIT_CARD').click();
    cy.get('#btn_create_order').should('exist').should('not.be.disabled');
    cy.get('#btn_create_order').click();
    cy.wait(200);
    cy.contains('La orden ha sido creada correctamente');

    cy.get('#btn_create_order').should('exist').should('be.disabled');
    cy.get('#order_create_total_amount').contains('0');
    cy.get('#order_created_product_selected_0').should('not.exist');
  });

  it('Create Order As Seller', () => {
    cy.login('seller@seller.com', '123456');
    cy.navigateToCreateOrder();

    cy.wait(1000);
    cy.contains('Crear Order');
    cy.get('#order_created_seller').should('not.exist');
    cy.contains('Cliente');
    cy.get('#order_created_client').should('exist');
    cy.contains('Fecha de Entrega');
    cy.get('#order_created_delivery_date').should('exist');
    cy.contains('Productos');
    cy.get('#order_created_products_label').should('exist');
    cy.get('#btn_open_product_stocks').should('exist');
    cy.contains('Método de Pago');
    cy.get('#paymentMethod_CREDIT_CARD').should('exist');
    cy.contains('Total');
    cy.get('#order_create_total_amount').contains('0');
    cy.get('#order_create_total_amount').should('exist');
    cy.contains('Crear');
    cy.get('#btn_create_order').should('exist').should('be.disabled');

    cy.get('#order_created_client').select('client (client@client.com)');
    cy.wait(500);

    cy.get('#btn_open_product_stocks').click();
    cy.get('#btn_create_order_previous_stock_page').should('exist');
    cy.get('#btn_create_order_next_stock_page').should('exist');
    cy.get('#create_order_checkbox_0').should('exist')
      .check()
      .should('be.checked');
    cy.wait(200);
    cy.get('#create_order_btn_increase_0').should('exist').should('not.be.disabled');
    cy.get('#create_order_btn_decrease_0').should('exist').should('be.disabled');
    cy.get('#create_order_btn_increase_0').click().click();
    cy.get('#create_order_btn_decrease_0').should('not.be.disabled').click();
    cy.get('#btn_create_order_add_products').should('exist').click();

    cy.get('#order_created_product_selected_0').should('exist');
    cy.get('#order_create_total_amount').should('not.contain', '0');
    cy.get('#create_order_btn_increase_quantity_0').should('exist').should('not.be.disabled').click();
    cy.get('#create_order_btn_decrease_quantity_0').should('exist').should('not.be.disabled').click().click();
    cy.get('#create_order_btn_decrease_quantity_0').should('exist').should('be.disabled');

    cy.get('#paymentMethod_CREDIT_CARD').click();
    cy.get('#btn_create_order').should('exist').should('not.be.disabled');
    cy.get('#btn_create_order').click();
    cy.wait(200);
    cy.contains('La orden ha sido creada correctamente');

    cy.get('#btn_create_order').should('exist').should('be.disabled');
    cy.get('#order_create_total_amount').contains('0');
    cy.get('#order_created_product_selected_0').should('not.exist');
  });
});