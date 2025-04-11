import { TestBed } from '@angular/core/testing';

import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SellerService } from './seller.service';
import { PaginatedSellers } from '../dtos/seller.dto';
import { environment } from 'src/environments/environment';


describe('SellerService', () => {
  let service: SellerService;
  let httpMock: HttpTestingController;


  const mockResponse: PaginatedSellers = {
    data: [
      {
        id: '051a514d-75a6-4525-9acc-fc7f36c659a7',
        name: 'Camilo 5',
        email: 'camilo5@sta.com',
        phone: '+573000000005',
        zone: 'CENTER',
        currency_quota: 'COP',
        currency_target: 'COP',
        quartely_target: 2000000.0,
        quota_expected: 1000000.0,
        performance_recomendations: "don't be a bad boy",
        user_id: 'c93593b7-769c-4f6e-a13d-b1653579cb95',
        created_at: '2025-04-09T23:05:33.282249',
        updated_at: '2025-04-09T23:05:33.282249',
        password: '123456',
        type:'TYPE'
      }
    ],
    page: 1,
    per_page: 10,
    total: 1,
    total_pages: 1
  };
  let userManagerAPI = environment.apiUserSessionUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SellerService]
    });
    service = TestBed.inject(SellerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Ensures no outstanding requests
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  it('should fetch sellers with default pagination', () => {
    service.getSellersPaginated().subscribe((res) => {
      expect(res).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(userManagerAPI+'/sellers/pag?page=1&per_page=10&sort_by=name&sort_order=asc');
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should fetch sellers with custom pagination', () => {
    service.getSellersPaginated(1, 10).subscribe((res) => {
      expect(res.page).toBe(1); // You can adjust this depending on mock
      expect(res.data.length).toBe(1);
    });

    const req = httpMock.expectOne(userManagerAPI+'/sellers/pag?page=1&per_page=10&sort_by=name&sort_order=asc');
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });
});
