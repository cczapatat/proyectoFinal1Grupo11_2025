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
import { UserSesionLoginComponent } from './user-session-login.component';

describe('UserLoginComponent', () => {
  let component: UserSesionLoginComponent;
  let fixture: ComponentFixture<UserSesionLoginComponent>;
  let debug: DebugElement;

  let userSessionService: jasmine.SpyObj<SessionManager>;
  let router: Router;

  beforeEach(() => {
    const usuarioServiceSpy = jasmine.createSpyObj('UsuarioService', ['login']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule.withRoutes([]),
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        ReactiveFormsModule,
      ],
      providers: [
        {
          provide: SessionManager,
          useValue: usuarioServiceSpy,
        },
        {
          provide: ToastrService,
          useValue: { success: jasmine.createSpy()}
        },
        FormBuilder,
      ],
      declarations: [UserSesionLoginComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(UserSesionLoginComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;
    userSessionService = TestBed.inject(SessionManager) as jasmine.SpyObj<SessionManager>;
    router = TestBed.get(Router); 
  });

  beforeEach(() => {
    userSessionService.login.and.returnValue(of({
      mensaje: 'Inicio de sesion exitoso',
      token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODM5MTI2NywianRpIjoiNDBlOTlmMDMtOWI4Ny00ZTUxLTgyMTktZjQwNDhlNDk0NjM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwiaWRfcHJvcGlldGFyaW8iOjAsImlzX2FkbWluIjp0cnVlfSwibmJmIjoxNzA4MzkxMjY3LCJjc3JmIjoiZjI5NzA1NTQtYTY0Ny00NzFlLTg1NDMtZWJjYmQ0OWVmMGFjIiwiZXhwIjoxNzA4MzkyMTY3fQ.dmoVsRgj2KAscG0EDpRLVZv21D3qzhkv-TOqvKnJ0og',
      id: 1,
      idPropietario: 0,
      isAdmin: true,
    }));
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has a title and description", () => {
    let title = debug.query(By.css('h2.my-2')).nativeElement;
    expect(title.innerHTML).toBe("Corta Estancia");

    let description = debug.query(By.css('p.my-2')).nativeElement;
    expect(description.innerHTML).toBe("Administrador de propiedades de corta estancia");
  });

  it("Component has 1 <input.tab-1> with id tab-1 element", () => {
    expect(debug.queryAll(By.css('#tab-1'))).toHaveSize(1);
  });

  it("Component has 1 <input.tab-2> with id tab-2 element", () => {
    expect(debug.queryAll(By.css('#tab-2'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id usuario element", () => {
    expect(debug.queryAll(By.css('#usuario'))).toHaveSize(1);
  });

  it("Should see usuario-requerido label", () => {
    expect(debug.queryAll(By.css('#usuario-requerido'))).toHaveSize(0);
    component.loginForm.controls['usuario'].setValue('');
    component.loginForm.controls['usuario'].markAsTouched();

    const usuario = component.loginForm.controls['usuario'];
    expect(usuario.valid).toBeFalsy();

    fixture.detectChanges();
    expect(usuario.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#usuario')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#usuario-requerido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id contrasena element", () => {
    expect(debug.queryAll(By.css('#contrasena'))).toHaveSize(1);
  });

  it("Should see contrasena-requerida label", () => {
    expect(debug.queryAll(By.css('#contrasena-requerida'))).toHaveSize(0);
    component.loginForm.controls['contrasena'].setValue('');
    component.loginForm.controls['contrasena'].markAsTouched();

    const contrasena = component.loginForm.controls['contrasena'];
    expect(contrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(contrasena.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#contrasena')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#contrasena-requerida'))).toHaveSize(1);
  });

  it("Component has 1 <button.btn.btn-info.col-8>  for signin usuario", () => {
    expect(debug.queryAll(By.css('button.btn.btn-info.col-8'))).toHaveSize(1);
  });

  it("Should see error-login label", () => {
    expect(debug.queryAll(By.css('#error-login'))).toHaveSize(0);
    component.error = "unexpected error"

    fixture.detectChanges();

    expect(debug.queryAll(By.css('#error-login'))).toHaveSize(1);
  });

  it("Should login correct", fakeAsync(() => {
    const navigateSpy = spyOn(router, 'navigate')

    const userNick = faker.hacker.phrase();
    const password = faker.hacker.verb();
    component.loginForm.controls['usuario'].setValue(userNick);
    component.loginForm.controls['contrasena'].setValue(password);

    fixture.detectChanges();

    const button = debug.nativeElement.querySelector('#doLogin');
    button.click();
    tick();

    expect(sessionStorage.getItem('idUsuario')).toEqual('1');
    expect(sessionStorage.getItem('idPropietario')).toEqual('0');
    expect(sessionStorage.getItem('isAdmin')).toEqual('true');
    expect(navigateSpy).toHaveBeenCalledWith(['/propiedades']);
  }));
});
