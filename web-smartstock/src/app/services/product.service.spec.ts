import { faker } from '@faker-js/faker';
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ProductService } from './product.service';

import { environment } from '../../environments/environment';
import { Product } from '../product/product';
import { ProductCategory } from '../dtos/product-category';

describe('Service: Product', () => {
  let service: ProductService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ProductService]
    });

    service = TestBed.inject(ProductService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should create a product', () => {
    const mockProduct: Product = {
      id: faker.string.uuid(),
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      unit_price: faker.number.float({ min: 1, max: 1000 }),
      discount_price: faker.number.float({ min: 1, max: 1000 }),
      currency_price: 'USD',
      category: 'ELECTRONICS',
      manufacturer_id: faker.string.uuid(),
      is_promotion: true,
      expired_at: faker.date.future().toISOString(),
      url_photo: faker.image.url(),
      store_conditions: faker.lorem.word({ length: 10 })
    };

    service.createProduct(mockProduct).subscribe((response) => {
      expect(response).toEqual(mockProduct);
    });

    const req = httpMock.expectOne(`${environment.apiProductUrl}/create`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(mockProduct);
    req.flush(mockProduct); // Simulate a successful response
  });

  it('should get a product by ID', () => {
    const productId = faker.string.uuid();
    const mockProduct: Product = {
      id: productId,
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      unit_price: faker.number.float({ min: 1, max: 1000 }),
      discount_price: faker.number.float({ min: 1, max: 1000 }),
      currency_price: 'USD',
      category: 'ELECTRONICS',
      manufacturer_id: faker.string.uuid(),
      is_promotion: true,
      expired_at: faker.date.future().toISOString(),
      url_photo: faker.image.url(),
      store_conditions: faker.lorem.word({ length: 10 })
    };

    service.getProductById(productId).subscribe((response) => {
      expect(response).toEqual(mockProduct);
    });

    const req = httpMock.expectOne(`${environment.apiProductUrl}/get/${productId}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockProduct);
  });

  it('should update a product', () => {
    const productId = faker.string.uuid();
    const mockProduct: Product = {
      id: productId,
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      unit_price: faker.number.float({ min: 1, max: 1000 }),
      discount_price: faker.number.float({ min: 1, max: 1000 }),
      currency_price: 'USD',
      category: 'ELECTRONICS',
      manufacturer_id: faker.string.uuid(),
      is_promotion: true,
      expired_at: faker.date.future().toISOString(),
      url_photo: faker.image.url(),
      store_conditions: faker.lorem.word({ length: 10 })
    };

    service.updateProduct(productId, mockProduct).subscribe((response) => {
      expect(response).toEqual(mockProduct);
    });

    const req = httpMock.expectOne(`${environment.apiProductUrl}/update/${productId}`);
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual(mockProduct);
    req.flush(mockProduct);
  });

  it('should get product categories', () => {
    const mockCategories: ProductCategory[] = [
      { key: 'electronics', value: 'Electronics' },
      { key: 'furniture', value: 'Furniture' }
    ];

    service.getProductCategories().subscribe((response) => {
      expect(response).toEqual(mockCategories);
    });

    const req = httpMock.expectOne(`${environment.apiProductUrl}/categories`);
    expect(req.request.method).toBe('GET');
    req.flush(mockCategories);
  });

  it('should get product currencies', () => {
    const mockCurrencies: ProductCategory[] = [
      { key: 'USD', value: 'US Dollar' },
      { key: 'EUR', value: 'Euro' }
    ];

    service.getProductCurrencies().subscribe((response) => {
      expect(response).toEqual(mockCurrencies);
    });

    const req = httpMock.expectOne(`${environment.apiProductUrl}/currencies`);
    expect(req.request.method).toBe('GET');
    req.flush(mockCurrencies);
  });
});