import { Component } from '@angular/core';
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { By } from '@angular/platform-browser';
import { of, throwError } from 'rxjs';
import { ToastrModule } from 'ngx-toastr';
import { RouterTestingModule } from '@angular/router/testing';
import { TranslateModule, TranslateLoader, TranslateService } from '@ngx-translate/core';
import { Observable, of as observableOf } from 'rxjs';

import { UserSessionLoginComponent } from './user-session-login.component';
import { SessionManager } from '../../services/session-manager.service';

// Dummy component for routing
@Component({ template: '' })
class DummyComponent {}

// A simple fake loader (not strictly necessary when using setTranslation below)
export class FakeLoader implements TranslateLoader {
  getTranslation(lang: string): Observable<any> {
    return observableOf({
      LOGIN: {
        TITLE: 'Log In Title (Fake)',
        EMAIL_LABEL: 'Email (Fake)',
        EMAIL_PLACEHOLDER: 'Email (Fake)',
        EMAIL_REQUIRED: 'The email is required in tests',
        EMAIL_INVALID: 'Invalid email format in tests',
        PASSWORD_LABEL: 'Password (Fake)',
        PASSWORD_PLACEHOLDER: '********* (Fake)',
        PASSWORD_REQUIRED: 'The password is required in tests',
        PASSWORD_MAX_LENGTH: 'The password can’t exceed 50 chars in tests',
        PASSWORD_MIN_LENGTH: 'The password must be > 4 chars in tests',
        BUTTON_LOGIN: 'Log In (Fake)',
        LOGIN_ERROR: 'Incorrect Email or Password (Fake)'
      }
    });
  }
}

describe('UserSessionLoginComponent', () => {
  let component: UserSessionLoginComponent;
  let fixture: ComponentFixture<UserSessionLoginComponent>;
  let sessionSpy: jasmine.SpyObj<SessionManager>;
  let translateService: TranslateService;
  let router: any;

  beforeEach(async () => {
    // Create a SpyObj for SessionManager with the required methods.
    sessionSpy = jasmine.createSpyObj('SessionManager', [
      'isSessionActive',
      'isSessionValid',
      'login',
      'saveSession'
    ]);
    sessionSpy.isSessionActive.and.returnValue(false);
    sessionSpy.isSessionValid.and.returnValue(of(false));
    sessionSpy.login.and.returnValue(of({ token: 'dummy-token' }));
    sessionSpy.saveSession.and.stub();

    await TestBed.configureTestingModule({
      declarations: [UserSessionLoginComponent, DummyComponent],
      imports: [
        ReactiveFormsModule,
        ToastrModule.forRoot(),
        RouterTestingModule.withRoutes([{ path: 'home', component: DummyComponent }]),
        TranslateModule.forRoot({
          loader: { provide: TranslateLoader, useClass: FakeLoader }
        })
      ],
      providers: [
        { provide: SessionManager, useValue: sessionSpy }
      ]
    }).compileComponents();

    router = TestBed.inject(RouterTestingModule);
    translateService = TestBed.inject(TranslateService);
    // Set translation for 'en' so that the pipe returns proper values.
    translateService.setTranslation('en', {
      LOGIN: {
        TITLE: 'Log In Title (Fake)',
        EMAIL_LABEL: 'Email (Fake)',
        EMAIL_PLACEHOLDER: 'Email (Fake)',
        EMAIL_REQUIRED: 'The email is required in tests',
        EMAIL_INVALID: 'Invalid email format in tests',
        PASSWORD_LABEL: 'Password (Fake)',
        PASSWORD_PLACEHOLDER: '********* (Fake)',
        PASSWORD_REQUIRED: 'The password is required in tests',
        PASSWORD_MAX_LENGTH: 'The password can’t exceed 50 chars in tests',
        PASSWORD_MIN_LENGTH: 'The password must be > 4 chars in tests',
        BUTTON_LOGIN: 'Log In (Fake)',
        LOGIN_ERROR: 'Incorrect Email or Password (Fake)'
      }
    });
    translateService.use('en');
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserSessionLoginComponent);
    component = fixture.componentInstance;
    // Ensure loginForm is a FormGroup with "email" and "password" controls.
    if (!(component.loginForm instanceof FormGroup)) {
      component.loginForm = new FormGroup({
        email: new FormControl(''),
        password: new FormControl('')
      });
    }
    fixture.detectChanges();
  });

  it('should create the login component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize loginForm with email and password controls', () => {
    expect(component.loginForm).toBeDefined();
    expect(component.loginForm.get('email')).toBeTruthy();
    expect(component.loginForm.get('password')).toBeTruthy();
  });

  it('should display required error for email when empty and touched', () => {
    const emailControl = component.loginForm.get('email');
    emailControl?.markAsTouched();
    fixture.detectChanges();
    const errorMsg = fixture.debugElement.query(By.css('#email-required'));
    expect(errorMsg).toBeTruthy();
    expect(errorMsg.nativeElement.textContent).toContain('The email is required in tests');
  });

  it('should display pattern error for email when format is invalid', () => {
    const emailControl = component.loginForm.get('email');
    emailControl?.setValue('invalidEmail');
    fixture.detectChanges();
    const errorMsg = fixture.debugElement.query(By.css('#correo-invalido'));
    expect(errorMsg).toBeTruthy();
    expect(errorMsg.nativeElement.textContent).toContain('Invalid email format in tests');
  });

  it('should display required error for password when empty and touched', () => {
    const passwordControl = component.loginForm.get('password');
    passwordControl?.markAsTouched();
    fixture.detectChanges();
    const errorMsg = fixture.debugElement.query(By.css('#password-required'));
    expect(errorMsg).toBeTruthy();
    expect(errorMsg.nativeElement.textContent).toContain('The password is required in tests');
  });

  it('should call loginUser on form submit when form is valid', () => {
    spyOn(component, 'loginUser').and.callThrough();
    component.loginForm.patchValue({
      email: 'test@example.com',
      password: 'password123'
    });
    fixture.detectChanges();
    const formEl = fixture.debugElement.query(By.css('#formLogin'));
    formEl.triggerEventHandler('ngSubmit', null);
    expect(component.loginUser).toHaveBeenCalledWith(component.loginForm.value);
  });
});