import { faker } from '@faker-js/faker';
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ProductService } from './product.service';

import { environment } from '../../environments/environment';
import { DocumentManagerService } from './document-manager.service';
import { Document } from '../massive/document';

describe('Service: Document Manager', () => {
  let service: DocumentManagerService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ProductService]
    });

    service = TestBed.inject(DocumentManagerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should upload a file', () => {
    const mockFile = new File([''], 'test-file.txt', { type: 'text/plain' });
    const mockDocument = new Document(
      faker.string.uuid(),
      faker.system.fileName(),
      faker.system.filePath(),
      faker.string.uuid(),
      faker.date.past().toString(),
      faker.date.past().toString()
    )


    service.uploadFile(mockFile).subscribe((response) => {
      expect(response).toEqual(mockDocument);
    });

    const req = httpMock.expectOne(`${environment.apiDocumentManagerUrl}/document/create`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body.get('file')).toEqual(mockFile);
    req.flush(mockDocument); // Simulate a successful response
  });
});