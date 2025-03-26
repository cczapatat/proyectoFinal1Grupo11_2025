/* tslint:disable:no-unused-variable */

import { TestBed, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from "@angular/common/http/testing";
import { UserSessionService } from './user-session.service';

describe('Service: Usuario', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserSessionService]
    });
  });

  it('should ...', inject([UserSessionService], (service: UserSessionService) => {
    expect(service).toBeTruthy();
  }));
});
