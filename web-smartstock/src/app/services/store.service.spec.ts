import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { StoreService } from './store.service';
import { environment } from '../../environments/environment';
import { StoreDto } from '../dtos/store.dto';

describe('StoreService', () => {
  let service: StoreService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiStoresUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [StoreService]
    });
    service = TestBed.inject(StoreService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get states', () => {
    const mockStates = ['ACTIVE', 'INACTIVE'];

    service.getStates().subscribe(states => {
      expect(states).toEqual(mockStates);
    });

    const req = httpMock.expectOne(`${apiUrl}/all-states`);
    expect(req.request.method).toBe('GET');
    req.flush(mockStates);
  });

  it('should get security levels', () => {
    const mockSecurityLevels = ['HIGH', 'MEDIUM', 'LOW'];

    service.getSecurityLevels().subscribe(levels => {
      expect(levels).toEqual(mockSecurityLevels);
    });

    const req = httpMock.expectOne(`${apiUrl}/all-security-levels`);
    expect(req.request.method).toBe('GET');
    req.flush(mockSecurityLevels);
  });

  it('should register store', () => {
    const mockStore = new StoreDto(
      'Test Store',
      '12345678901',
      'test@store.com',
      'Test Address',
      100,
      'ACTIVE',
      'HIGH'
    );

    const mockResponse = {
      id: 'uuid',
      name: 'Test Store',
      phone: '12345678901',
      email: 'test@store.com',
      address: 'Test Address',
      capacity: 100,
      state: 'ACTIVE',
      security_level: 'HIGH'
    };

    service.registerStore(mockStore).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/create`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(mockStore);
    req.flush(mockResponse);
  });

  it('should include default headers in all requests', () => {
    service.getStates().subscribe();

    const req = httpMock.expectOne(`${apiUrl}/all-states`);
    expect(req.request.headers.has('x-token')).toBeTrue();
  });
});
