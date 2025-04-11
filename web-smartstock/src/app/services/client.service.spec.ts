import { TestBed } from '@angular/core/testing';

import { ClientService } from './client.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { PaginatedClients } from '../dtos/client';
import { environment } from 'src/environments/environment';

describe('ClientService', () => {
  let service: ClientService;
  let httpMock: HttpTestingController;

  const dummyResponse: PaginatedClients = {
    data: [
      {
        id: '1',
        name: 'Pedro Herrera',
        email: 'pedro1@sta.com',
        phone: '+573017084101',
        address: 'AV 123',
        client_type: 'CORNER_STORE',
        zone: 'CENTER',
        user_id: 'user-1',
        created_at: 'Wed, 09 Apr 2025 12:02:01 GMT',
        updated_at: 'Wed, 09 Apr 2025 12:02:01 GMT',
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
      providers: [ClientService]
    });
    service = TestBed.inject(ClientService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch clients by seller ID with pagination and sorting', () => {
    const sellerId = 'seller-123';
    const page = 1;
    const perPage = 10;
    const sortBy = 'name';
    const sortOrder = 'asc';

    service.getClientsBySellerId(sellerId, page, perPage, sortBy, sortOrder).subscribe((res) => {
      expect(res).toEqual(dummyResponse);
      expect(res.data.length).toBe(1);
      expect(res.data[0].name).toBe('Pedro Herrera');
    });

    const req = httpMock.expectOne(
      `${userManagerAPI}/clients/seller/${sellerId}?page=${page}&per_page=${perPage}&sort_by=${sortBy}&sort_order=${sortOrder}`
    );
    expect(req.request.method).toBe('GET');
    req.flush(dummyResponse);
  });
});
