/* tslint:disable:no-unused-variable */

import { TestBed, inject } from '@angular/core/testing';
import { EnumsService } from './enums.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('Service: EnumsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [EnumsService]
    });
  });

  it('should ...', inject([EnumsService], (service: EnumsService) => {
    expect(service).toBeTruthy();
  }));
});
