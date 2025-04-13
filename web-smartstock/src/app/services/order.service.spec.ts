import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { OrderService } from './order.service';
import { environment } from '../../environments/environment';
import { OrderCreateDTO, ProductStockCreateDTO, OrderCreatedDTO, ProductStockCreatedDTO } from '../dtos/order.dto';

describe('OrderService', () => {
  let service: OrderService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiOrderUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OrderService]
    });
    service = TestBed.inject(OrderService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get payment methods', () => {
    const mockPaymentMethods = ['PAYMENT_ON_DELIVERY', 'CREDIT_CARD', 'DEBIT_CARD'];

    service.getPaymentMethods().subscribe(states => {
      expect(states).toEqual(mockPaymentMethods);
    });

    const req = httpMock.expectOne(`${apiUrl}/all-payment-methods`);
    expect(req.request.method).toBe('GET');
    req.flush(mockPaymentMethods);
  });

  it('should include default headers in all requests', () => {
    service.getPaymentMethods().subscribe();

    const req = httpMock.expectOne(`${apiUrl}/all-payment-methods`);
    expect(req.request.headers.has('x-token')).toBeTrue();
  });

  it('should create order', () => {
    const productStocksMock: ProductStockCreateDTO[] = [
      { product_id: 'uuid', units: 10 },
      { product_id: 'uuid2', units: 5 }
    ];
    const mockOrder = new OrderCreateDTO(
      'uuid',
      '2025-06-09 00:00:00',
      'CREDIT_CARD',
      productStocksMock,
    );

    const mockResponse: OrderCreatedDTO = new OrderCreatedDTO(
      'uuid',
      'uuid',
      '2025-06-09 00:00:00',
      'CREDIT_CARD',
      productStocksMock.map(stock => new ProductStockCreatedDTO(
        'uuid',
        'uuid',
        stock.product_id,
        stock.units,
        '2023-10-01T12:00:00Z',
        '2023-10-01T12:00:00Z'
      )),
      'uuid',
      'ACTIVE',
      100,
      'uuid',
      '2023-10-01T12:00:00Z',
      '2023-10-01T12:00:00Z'
    );

    service.createOrder(mockOrder).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/create`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(mockOrder);
    req.flush(mockResponse);
  });
});
