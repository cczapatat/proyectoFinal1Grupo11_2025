/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HeaderComponent } from './header.component';
import { DebugElement } from '@angular/core';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule } from 'ngx-toastr';
import { SessionManager } from 'src/app/services/session-manager.service';
import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';
import { TranslateModule, TranslateService } from '@ngx-translate/core';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: ComponentFixture<HeaderComponent>;
  let debug: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        TranslateModule.forRoot(),
      ],
      providers: [
        SessionManager,
        JwtHelperService,
        { provide: JWT_OPTIONS, useValue: {} },
        TranslateService
      ],
      declarations: [ HeaderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
