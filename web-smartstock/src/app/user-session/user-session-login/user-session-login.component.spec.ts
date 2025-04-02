import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { faker } from '@faker-js/faker';
import { of } from 'rxjs';
import { Router } from '@angular/router';

import { SessionManager } from '../../services/session-manager.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { UserSessionLoginComponent } from './user-session-login.component';

describe('UserSessionLoginComponent', () => {
  let component: UserSessionLoginComponent;
  let fixture: ComponentFixture<UserSessionLoginComponent>;
  let debug: DebugElement;
  let sessionManager: jasmine.SpyObj<SessionManager>;
  let router: Router;

  beforeEach(async () => {
    // Create the spy for SessionManager with the required methods.
    const sessionManagerSpy = jasmine.createSpyObj('SessionManager', [
      'login',
      'guardarSesion',
      'esSesionValida',
      'esSesionActiva',
    ]);

    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule.withRoutes([]),
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        ReactiveFormsModule,
      ],
      providers: [
        { provide: SessionManager, useValue: sessionManagerSpy },
        { provide: ToastrService, useValue: { success: jasmine.createSpy() } },
        FormBuilder,
      ],
      declarations: [UserSessionLoginComponent],
    }).compileComponents();

    // Set default spy return values BEFORE creating the component.
    sessionManager = TestBed.inject(SessionManager) as jasmine.SpyObj<SessionManager>;
    router = TestBed.inject(Router);
    sessionManager.login.and.returnValue(
      of({
        mensaje: 'Inicio de sesion exitoso',
        token: 'sample-token',
        userId: '1',
        type: 'true',
      })
    );
    // By default, have esSesionValida and esSesionActiva return false.
    sessionManager.esSesionValida.and.returnValue(of(false));
    sessionManager.esSesionActiva.and.returnValue(false);

    fixture = TestBed.createComponent(UserSessionLoginComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    // Now trigger ngOnInit and initial() with our spy methods in place.
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display the title "Sign Up As Seller"', () => {
    const titleElem = debug.query(By.css('h2.my-2')).nativeElement;
    expect(titleElem.textContent).toContain('Sign Up As Seller');
  });

  it('should have an input for email with id="email"', () => {
    const emailField = debug.query(By.css('#email'));
    expect(emailField).toBeTruthy();
  });

  it('should display #email-required error when email is empty and touched', () => {
    component.loginForm.controls['email'].setValue('');
    component.loginForm.controls['email'].markAsTouched();
    fixture.detectChanges();

    const emailCtrl = component.loginForm.controls['email'];
    expect(emailCtrl.hasError('required')).toBeTrue();

    const emailRequiredElem = debug.query(By.css('#email-required'));
    expect(emailRequiredElem).toBeTruthy();
  });

  it('should have an input for password with id="password"', () => {
    const passwordField = debug.query(By.css('#password'));
    expect(passwordField).toBeTruthy();
  });

  it('should display #password-required error when password is empty and touched', () => {
    component.loginForm.controls['password'].setValue('');
    component.loginForm.controls['password'].markAsTouched();
    fixture.detectChanges();

    const passCtrl = component.loginForm.controls['password'];
    expect(passCtrl.hasError('required')).toBeTrue();

    const passwordReqElem = debug.query(By.css('#password-required'));
    expect(passwordReqElem).toBeTruthy();
  });

  it('should have a login button with id="doLogin"', () => {
    const loginButton = debug.query(By.css('#doLogin'));
    expect(loginButton).toBeTruthy();
  });

  it('should display #error-login when error is set', () => {
    expect(debug.query(By.css('#error-login'))).toBeFalsy(); // Initially hidden
    component.error = 'Some login error';
    fixture.detectChanges();

    const errorElem = debug.query(By.css('#error-login'));
    expect(errorElem).toBeTruthy();
  });

  it('should perform login and navigate to "/home" if session is valid', fakeAsync(() => {
    const navigateSpy = spyOn(router, 'navigate');
    // Make the session checks pass.
    sessionManager.esSesionValida.and.returnValue(of(true));
    sessionManager.esSesionActiva.and.returnValue(true);

    const testEmail = faker.internet.email();
    const testPassword = faker.internet.password();
    component.loginForm.controls['email'].setValue(testEmail);
    component.loginForm.controls['password'].setValue(testPassword);
    fixture.detectChanges();

    const loginButton = debug.nativeElement.querySelector('#doLogin');
    loginButton.click();
    tick();

    // Verify that guardarSesion is called with the expected parameters.
    expect(sessionManager.guardarSesion).toHaveBeenCalledWith('sample-token', '1', 'true');
    // Verify navigation to '/home'.
    expect(navigateSpy).toHaveBeenCalledWith(['/home']);
  }));
});