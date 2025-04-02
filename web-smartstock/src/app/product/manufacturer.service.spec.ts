/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ManufacturerService } from './manufacturer.service';

describe('Service: Manufacturer', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ManufacturerService]
    });
  });

  it('should ...', inject([ManufacturerService], (service: ManufacturerService) => {
    expect(service).toBeTruthy();
  }));
});
