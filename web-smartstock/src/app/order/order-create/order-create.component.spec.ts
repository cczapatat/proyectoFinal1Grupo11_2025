import { DebugElement } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OrderService } from 'src/app/services/order.service';
import { ClientService } from 'src/app/services/client.service';
import { SellerService } from 'src/app/services/seller.service';
import { StocksService } from 'src/app/services/stocks.service';
import { OrderCreateComponent } from './order-create.component';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule } from 'ngx-toastr';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { of } from 'rxjs';
import { OrderCreatedDTO } from 'src/app/dtos/order.dto';
import { By } from '@angular/platform-browser';

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

describe('OrderCreateComponent', () => {
  let component: OrderCreateComponent;
  let fixture: ComponentFixture<OrderCreateComponent>;
  let debug: DebugElement;

  let clientService: jasmine.SpyObj<ClientService>;
  let sellerService: jasmine.SpyObj<SellerService>;
  let stocksService: jasmine.SpyObj<StocksService>;
  let orderService: jasmine.SpyObj<OrderService>;


  beforeEach(async () => {
    const clientServiceMock = jasmine.createSpyObj('ClientService', ['getClientsBySellerIdList']);
    const sellerServiceMock = jasmine.createSpyObj('SellerService', ['getSellersList']);
    const stocksServiceMock = jasmine.createSpyObj('StocksService', ['getProductsOnStock']);
    const orderServiceMock = jasmine.createSpyObj('OrderService', ['getPaymentMethods', 'createOrder']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ReactiveFormsModule,
        FormsModule,
        TranslateModule.forRoot(),
        ToastrModule.forRoot(),
      ],
      providers: [
        TranslateService,
        { provide: ClientService, useValue: clientServiceMock },
        { provide: SellerService, useValue: sellerServiceMock },
        { provide: StocksService, useValue: stocksServiceMock },
        { provide: OrderService, useValue: orderServiceMock },
      ],
      declarations: [OrderCreateComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(OrderCreateComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    clientService = TestBed.inject(ClientService) as jasmine.SpyObj<ClientService>;
    sellerService = TestBed.inject(SellerService) as jasmine.SpyObj<SellerService>;
    stocksService = TestBed.inject(StocksService) as jasmine.SpyObj<StocksService>;
    orderService = TestBed.inject(OrderService) as jasmine.SpyObj<OrderService>;
  });

  beforeEach(() => {
    localStorage.setItem('user_id', 'uuid');
    localStorage.setItem('type', 'ADMIN');
    clientService.getClientsBySellerIdList.and.returnValue(of([
      { id: 'uuid1', name: 'Client 1', phone: '', email: '', address: '', client_type: 'TEST', zone: 'CENTER', created_at: '', updated_at: '' },
      { id: 'uuid2', name: 'Client 2', phone: '', email: '', address: '', client_type: 'TEST', zone: 'CENTER', created_at: '', updated_at: '' },
    ]));
    sellerService.getSellersList.and.returnValue(of([
      { id: 'uuid3', name: 'Seller 1', phone: '', email: 'seller1@test.com', password: '', user_id: 'uuid5', type: '', zone: 'CENTER', quota_expected: 0, currency_quota: 'COP', quartely_target: 0, currency_target: 'COP', performance_recomendations: '', created_at: '', updated_at: '' },
      { id: 'uuid4', name: 'Seller 2', phone: '', email: 'seller2@test.com', password: '', user_id: 'uuid6', type: '', zone: 'CENTER', quota_expected: 0, currency_quota: 'COP', quartely_target: 0, currency_target: 'COP', performance_recomendations: '', created_at: '', updated_at: '' }
    ]));
    stocksService.getProductsOnStock.and.returnValue(of({
      page: 1,
      per_page: 5,
      total: 2,
      stocks: [
        { id: 'uuid7', quantity_in_stock: 10, last_quantity: 12, enabled: true, update_date: '', creation_date: '', product: { id: 'uuid8', manufacturer_id: 'uuid9', name: '1', description: '', category: '', unit_price: 10, currency_price: 'COP', is_promotion: false, discount_price: 1, expired_at: null, url_photo: 'http://photo.com', store_conditions: '' } },
        { id: 'uuid10', quantity_in_stock: 10, last_quantity: 12, enabled: true, update_date: '', creation_date: '', product: { id: 'uuid11', manufacturer_id: 'uuid12', name: '2', description: '', category: '', unit_price: 10, currency_price: 'COP', is_promotion: false, discount_price: 1, expired_at: null, url_photo: 'http://photo.com', store_conditions: '' } },
      ]
    }));
    orderService.getPaymentMethods.and.returnValue(of(['PAYMENT_ON_DELIVERY', 'CREDIT_CARD', 'DEBIT_CARD']));
    orderService.createOrder.and.returnValue(of(new OrderCreatedDTO('uuid13', 'uuid14', '2025/06/30 10:10:10', 'PAYMENT_ON_DELIVERY', [], 'uuid15', 'PENDING', 100, 'uuid16', '2025/06/30 10:10:10', '2025/06/30 10:10:10')));

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('Component has a title', () => {
    const title = debug.query(By.css('h2')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it('Exists seller select', () => {
    const select = debug.query(By.css('#order_created_seller'));
    expect(select).toBeTruthy();
  });

  it('Not Exists seller select', () => {
    localStorage.setItem('type', 'SELLER');
    
    fixture = TestBed.createComponent(OrderCreateComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;
    
    fixture.detectChanges();
    const select = debug.query(By.css('#order_created_seller'));
    expect(select).toBeFalsy();
  });

  it('Create order with success', async () => {
    const sellerSelect = debug.query(By.css('#order_created_seller')).nativeElement;
    sellerSelect.value = sellerSelect.options[1].value;
    sellerSelect.dispatchEvent(new Event('change'));
    fixture.detectChanges();

    expect(component.selectedSeller).toBe(sellerSelect.options[1].value);

    const sellerClient = debug.query(By.css('#order_created_client')).nativeElement;
    sellerClient.value = sellerClient.options[1].value;
    sellerClient.dispatchEvent(new Event('change'));
    fixture.detectChanges();

    expect(component.selectedClient).toBe(sellerClient.options[1].value);

    const openProductStocksButton = debug.query(By.css('#btn_open_product_stocks')).nativeElement;
    openProductStocksButton.click();
    fixture.detectChanges();

    const firstCheckbox = debug.query(By.css('input.pointer')).nativeElement;
    firstCheckbox.click();
    fixture.detectChanges();

    const addProductsToOrder = debug.query(By.css('#btn_create_order_add_products')).nativeElement;
    addProductsToOrder.click();
    fixture.detectChanges();

    const totalAmountSpan = debug.query(By.css('#order_create_total_amount')).nativeElement;
    expect(totalAmountSpan.textContent.trim()).toBe('100 COP');

    const firstPaymentMethod = debug.query(By.css('input#paymentMethod_CREDIT_CARD')).nativeElement;
    firstPaymentMethod.click();
    fixture.detectChanges();

    expect(component.selectedPayment).toBe('CREDIT_CARD');
    expect(component.deliveryDate).not.toBe('');
    expect(component.validOrder).toBe(true);

    const btnCreateOrder = debug.query(By.css('#btn_create_order')).nativeElement;
    btnCreateOrder.click();
    fixture.detectChanges();
    await sleep(200);

    expect(orderService.createOrder).toHaveBeenCalled();
  })

  it('increment, decrement and remove product quantity main view', () => {
    const productStock = { quantitySelected: 10, id: 'uuid7', quantity_in_stock: 10, last_quantity: 12, enabled: true, update_date: '', creation_date: '', product: { id: 'uuid8', manufacturer_id: 'uuid9', name: '1', description: '', category: '', unit_price: 10, currency_price: 'COP', is_promotion: false, discount_price: 1, expired_at: null, url_photo: 'http://photo.com', store_conditions: '' } };
    component.products = [productStock];
    component.incrementQuantity(productStock);
    expect(productStock.quantitySelected).toBe(11);

    component.decrementQuantity(productStock);
    expect(productStock.quantitySelected).toBe(10);

    productStock.quantitySelected = 1;
    component.decrementQuantity(productStock);
    expect(productStock.quantitySelected).toBe(1);

    component.removeProduct(productStock);
    expect(component.products.length).toBe(0);
  })

  it('increment, decrement and remove product quantity modal view', () => {
    const selectedProducts = { 'uuidX': 1 };
    component.selectedModalProducts = selectedProducts;
    component.increaseModalQuantity('uuidX', 2);
    expect(component.selectedModalProducts['uuidX']).toBe(2);

    component.decreaseModalQuantity('uuidX');
    expect(component.selectedModalProducts['uuidX']).toBe(1);

    component.decreaseModalQuantity('uuidX');
    expect(component.selectedModalProducts['uuidX']).toBe(1);
  });
});
