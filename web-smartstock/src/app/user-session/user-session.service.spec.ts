/* tslint:disable:no-unused-variable */

import { TestBed, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from "@angular/common/http/testing";
import { SessionManager } from '../services/session-manager.service';
import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';

describe('Service: User Session', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        SessionManager,
        JwtHelperService,
        { provide: JWT_OPTIONS, useValue: {} }
      ],
    });
  });

  it('should ...', inject([SessionManager], (service: SessionManager) => {
    expect(service).toBeTruthy();
  }));
});
