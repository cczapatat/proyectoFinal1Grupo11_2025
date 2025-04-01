/* tslint:disable:no-unused-variable */

import { TestBed, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from "@angular/common/http/testing";
import { SessionManager } from '../services/session-manager.service';

describe('Service: Usuario', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SessionManager]
    });
  });

  it('should ...', inject([SessionManager], (service: SessionManager) => {
    expect(service).toBeTruthy();
  }));
});
