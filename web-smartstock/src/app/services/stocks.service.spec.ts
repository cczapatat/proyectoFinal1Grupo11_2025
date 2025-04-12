import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { StocksService } from './stocks.service';
import { environment } from 'src/environments/environment';
import { AssignedStockDto } from '../dtos/assignedStock';

describe('StocksService', () => {
  let service: StocksService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [ StocksService ]
    });
    service = TestBed.inject(StocksService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getStocksByStore', () => {
    it('should perform a GET request and return assigned stocks', () => {
      const dummyResponse: AssignedStockDto = {
        store_id: 'store1',
        stocks: [
          { id: 'stock1', product_id: 'prod1', assigned_stock: 10 }
        ]
      };

      service.getStocksByStore('store1').subscribe(response => {
        expect(response.store_id).toEqual('store1');
        expect(response.stocks.length).toBe(1);
        expect(response.stocks[0].assigned_stock).toBe(10);
      });

      const req = httpMock.expectOne(`${environment.apiStocksUrl}/stocks/by-store-id?id_store=store1`);
      expect(req.request.method).toBe('GET');
      // Optionally, you can check for headers here if needed.
      req.flush(dummyResponse);
    });
  });

  describe('#assignStockToStore', () => {
    it('should perform a PUT request with the assigned stock DTO', () => {
      const dummyDto: AssignedStockDto = {
        store_id: 'store1',
        stocks: [
          { id: '', product_id: 'prod1', assigned_stock: 5 }
        ]
      };
      const dummyResponse = { success: true };

      service.assignStockToStore(dummyDto).subscribe(response => {
        expect(response.success).toBeTrue();
      });

      const req = httpMock.expectOne(`${environment.apiStocksUrl}/stocks/assign-stock-store`);
      expect(req.request.method).toBe('PUT');
      expect(req.request.body).toEqual(dummyDto);
      req.flush(dummyResponse);
    });
  });
});