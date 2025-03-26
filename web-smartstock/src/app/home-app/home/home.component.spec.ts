import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule } from 'ngx-toastr';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';
import { of } from 'rxjs';

import { PropiedadListaComponent } from './home.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ModalModule } from 'ngx-bootstrap/modal';

describe('HomeComponent', () => {
  let component: PropiedadListaComponent;
  let fixture: ComponentFixture<PropiedadListaComponent>;
  let debug: DebugElement;

  beforeEach(async () => {

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        ModalModule.forRoot(),
      ],
      providers: [
        {
          provide: ActivatedRoute, useValue: {
            snapshot: {
              paramMap: convertToParamMap({ 'id': 2 }),
            }
          },
        }
      ],
      declarations: [PropiedadListaComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(PropiedadListaComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;
  });

  beforeEach(() => {
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
