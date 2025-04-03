import { Component } from '@angular/core';
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { By } from '@angular/platform-browser';
import { of, throwError, Observable } from 'rxjs';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { RouterTestingModule } from '@angular/router/testing';
import { TranslateModule, TranslateLoader, TranslateService } from '@ngx-translate/core';
import { Router } from '@angular/router';

import { UserSessionSignUpComponent } from './user-session-sign-up.component';
import { SellerService } from 'src/app/services/seller.service';

// Dummy component for routing
@Component({ template: '' })
class DummyComponent {}

// FakeLoader for TranslateModule
export class FakeLoader implements TranslateLoader {
  getTranslation(lang: string): Observable<any> {
    return of({
      SIGNUP: {
        TITLE: "Register Salesperson",
        NAME_LABEL: "Name",
        NAME_PLACEHOLDER: "Name",
        NAME_REQUIRED: "Name is required.",
        NAME_MAX_LENGTH: "Name cannot exceed 255 characters.",
        PHONE_LABEL: "Phone",
        PHONE_PLACEHOLDER: "+573217830011",
        PHONE_REQUIRED: "Phone is required.",
        PHONE_MAX_LENGTH: "Phone cannot exceed 20 characters.",
        PHONE_PATTERN: "Phone must start with '+' and be valid.",
        EMAIL_LABEL: "Email",
        EMAIL_PLACEHOLDER: "modesty@gmail.com",
        EMAIL_REQUIRED: "Email is required.",
        EMAIL_INVALID: "Invalid email format.",
        EMAIL_MIN_LENGTH: "Email must be at least 10 characters.",
        EMAIL_MAX_LENGTH: "Email cannot exceed 255 characters.",
        PASSWORD_LABEL: "Password",
        PASSWORD_PLACEHOLDER: "*********",
        PASSWORD_REQUIRED: "Password is required.",
        PASSWORD_MIN_LENGTH: "Must be at least 5 characters.",
        PASSWORD_MAX_LENGTH: "Cannot exceed 50 characters.",
        CONFIRM_PASSWORD_LABEL: "Confirm Password",
        CONFIRM_PASSWORD_PLACEHOLDER: "*********",
        CONFIRM_PASSWORD_REQUIRED: "Confirming your password is required.",
        PASSWORD_MISMATCH: "Passwords do not match.",
        ZONE_LABEL: "Zone",
        ZONE_SELECTED: "Select a Zone",
        ZONE_REQUIRED: "Zone is required.",
        QUOTA_LABEL: "Expected Quota",
        QUOTA_PLACEHOLDER: "200,000",
        QUOTA_REQUIRED: "Expected quota is required.",
        QUOTA_MIN: "Must be a positive number.",
        CURRENCY_SELECTED: "Select",
        CURRENCY_REQUIRED: "Currency is required.",
        TARGET_LABEL: "Quarterly Target",
        TARGET_PLACEHOLDER: "600,000",
        TARGET_REQUIRED: "Quarterly target is required.",
        TARGET_MIN: "Must be a positive number.",
        PERFORMANCE_LABEL: "Performance recommendations",
        PERFORMANCE_PLACEHOLDER: "1. Know your product...",
        PERFORMANCE_REQUIRED: "This field is required.",
        BUTTON_SIGNUP: "Create",
        SUCCESS_MESSAGE: "Seller created successfully.",
        SUCCESS_TITLE: "Success",
        ERROR_MESSAGE: "An error occurred:",
        ERROR_TITLE: "Error"
      }
    });
  }
}

describe('UserSessionSignUpComponent', () => {
  let component: UserSessionSignUpComponent;
  let fixture: ComponentFixture<UserSessionSignUpComponent>;
  let sellerServiceSpy: jasmine.SpyObj<SellerService>;
  let toastrServiceSpy: jasmine.SpyObj<ToastrService>;
  let router: Router;
  let translateService: TranslateService;

  beforeEach(async () => {
    // Create spies for SellerService and ToastrService.
    sellerServiceSpy = jasmine.createSpyObj('SellerService', ['createSeller']);
    toastrServiceSpy = jasmine.createSpyObj('ToastrService', ['success', 'error']);

    await TestBed.configureTestingModule({
      declarations: [UserSessionSignUpComponent, DummyComponent],
      imports: [
        ReactiveFormsModule,
        RouterTestingModule.withRoutes([{ path: 'user-session/login', component: DummyComponent }]),
        ToastrModule.forRoot(),
        TranslateModule.forRoot({ loader: { provide: TranslateLoader, useClass: FakeLoader } })
      ],
      providers: [
        { provide: SellerService, useValue: sellerServiceSpy },
        { provide: ToastrService, useValue: toastrServiceSpy }
      ]
    }).compileComponents();

    router = TestBed.inject(Router);
    translateService = TestBed.inject(TranslateService);
    translateService.use('en'); // Use English translations
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserSessionSignUpComponent);
    component = fixture.componentInstance;
    // Ensure the sellerForm is initialized with all expected controls.
    if (!(component.sellerForm instanceof FormGroup)) {
      component.sellerForm = new FormGroup({
        name: new FormControl(''),
        phone: new FormControl(''),
        email: new FormControl(''),
        password: new FormControl(''),
        confirmPassword: new FormControl(''),
        zone: new FormControl(''),
        quotaExpected: new FormControl(''),
        currencyQuota: new FormControl(''),
        quarterlyTarget: new FormControl(''),
        currencyTarget: new FormControl(''),
        performanceRecomendations: new FormControl('')
      });
    }
    fixture.detectChanges();
  });

  it('should create the signup component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize sellerForm with all expected controls', () => {
    const controls = [
      'name', 'phone', 'email', 'password', 'confirmPassword', 'zone',
      'quotaExpected', 'currencyQuota', 'quarterlyTarget', 'currencyTarget',
      'performanceRecomendations'
    ];
    controls.forEach(control => {
      expect(component.sellerForm.get(control)).toBeTruthy();
    });
  });

  it('should not call createSeller if form is invalid', () => {
    // Set all required fields to empty
    component.sellerForm.patchValue({
      name: '',
      phone: '',
      email: '',
      password: '',
      confirmPassword: '',
      zone: '',
      quotaExpected: '',
      currencyQuota: '',
      quarterlyTarget: '',
      currencyTarget: '',
      performanceRecomendations: ''
    });
    fixture.detectChanges();
    sellerServiceSpy.createSeller.calls.reset();
    component.registerSeller(component.sellerForm.value);
    expect(sellerServiceSpy.createSeller).not.toHaveBeenCalled();
  });

  it('should call createSeller on valid form submission, show success toastr, reset form, and navigate to login', fakeAsync(() => {
    const validForm = {
      name: 'Test Seller',
      phone: '+1234567890',
      email: 'test@example.com',
      password: 'password123',
      confirmPassword: 'password123',
      zone: 'CENTER',
      quotaExpected: '200,000',
      currencyQuota: 'COP',
      quarterlyTarget: '600,000',
      currencyTarget: 'COP',
      performanceRecomendations: 'Be nice'
    };
    component.sellerForm.patchValue(validForm);
    fixture.detectChanges();

    sellerServiceSpy.createSeller.and.returnValue(of({ token: 'dummy-token' }));
    spyOn(router, 'navigate');

    component.registerSeller(component.sellerForm.value);
    tick();
    fixture.detectChanges();

    expect(sellerServiceSpy.createSeller).toHaveBeenCalled();
    expect(toastrServiceSpy.success).toHaveBeenCalledWith(
      translateService.instant('SIGNUP.SUCCESS_MESSAGE'),
      translateService.instant('SIGNUP.SUCCESS_TITLE'),
      { closeButton: true }
    );
    expect(router.navigate).toHaveBeenCalledWith(['/user-session/login']);
    // Check that the form is reset (all controls are null)
    expect(component.sellerForm.value).toEqual({
      name: null,
      phone: null,
      email: null,
      password: null,
      confirmPassword: null,
      zone: null,
      quotaExpected: null,
      currencyQuota: null,
      quarterlyTarget: null,
      currencyTarget: null,
      performanceRecomendations: null
    });
  }));

  it('should show error toastr when createSeller fails', fakeAsync(() => {
    const validForm = {
      name: 'Test Seller',
      phone: '+1234567890',
      email: 'test@example.com',
      password: 'password123',
      confirmPassword: 'password123',
      zone: 'CENTER',
      quotaExpected: '200,000',
      currencyQuota: 'COP',
      quarterlyTarget: '600,000',
      currencyTarget: 'COP',
      performanceRecomendations: 'Be nice'
    };
    component.sellerForm.patchValue(validForm);
    fixture.detectChanges();

    sellerServiceSpy.createSeller.and.returnValue(throwError(() => new Error('Signup failed')));

    component.registerSeller(component.sellerForm.value);
    tick();
    fixture.detectChanges();

    expect(toastrServiceSpy.error).toHaveBeenCalledWith(
      translateService.instant('SIGNUP.ERROR_MESSAGE') + ' ' + 'Signup failed',
      translateService.instant('SIGNUP.ERROR_TITLE'),
      { closeButton: true }
    );
  }));
});