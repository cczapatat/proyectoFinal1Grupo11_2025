/* tslint:disable:no-unused-variable */
import { fa, faker } from '@faker-js/faker';
import { TestBed, async, inject } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ManufacturerService } from './manufacturer.service';
import { Manufacturer } from '../dtos/manufacturer';
import { environment } from 'src/environments/environment';


describe('Service: Manufacturer', () => {
  let service: ManufacturerService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ManufacturerService]
    });

    service = TestBed.inject(ManufacturerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Ensure no outstanding HTTP requests
  });

  it('should get the list of manufacturers', () => {
    const mockManufacturers: Manufacturer[] = [
      {
        id: faker.string.uuid(),
        name: faker.company.name(),
        address: faker.address.streetAddress(),
        phone: faker.phone.number().toString(),
        email: faker.internet.email(),
        country: 'USA',
        rating_quality: faker.number.float({ min: 1, max: 5 }),
        tax_conditions: faker.lorem.word({ length: 10 }),
        legal_conditions:faker.lorem.word({ length: 10 }),
      },
      {
        id: faker.string.uuid(),
        name: faker.company.name(),
        address: faker.address.streetAddress(),
        phone: faker.phone.number().toString(),
        email: faker.internet.email(),
        country: 'USA',
        rating_quality: faker.number.float({ min: 1, max: 5 }),
        tax_conditions: faker.lorem.word({ length: 10 }),
        legal_conditions:faker.lorem.word({ length: 10 }),
      }
    ];

    service.getManufacturerList().subscribe((response) => {
      expect(response).toEqual(mockManufacturers);
    });

    const req = httpMock.expectOne(`${environment.apiManufacturerUrl}/manufacturers/all`);
    expect(req.request.method).toBe('GET');
    req.flush(mockManufacturers); // Simulate a successful response
  });
});
