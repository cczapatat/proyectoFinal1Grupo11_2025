import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { faker } from '@faker-js/faker';

import { UserSessionSignUpComponent } from './user-session-sign-up.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule } from 'ngx-toastr';
import { SessionManager } from '../../services/session-manager.service';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { UserSession } from '../user-session';
import { of } from 'rxjs';
import { EnumsService } from 'src/app/enums.service';

describe('UsuarioRegistroComponent', () => {
  let component: UserSessionSignUpComponent;
  let fixture: ComponentFixture<UserSessionSignUpComponent>;
  let debug: DebugElement;

  let usuarioService: jasmine.SpyObj<SessionManager>;
  let enumsService: jasmine.SpyObj<EnumsService>;

  let dummyUsuarios: UserSession[];

  const bancos = ['BANCO_BBVA', 'BANCO_AGRARIO'];

  beforeEach(() => {
    const enumsServiceSpy = jasmine.createSpyObj('EnumsService', ['bancos']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        ReactiveFormsModule,
      ],
      providers: [
        SessionManager,
        FormBuilder,
        {
          provide: EnumsService,
          useValue: enumsServiceSpy,
        }
      ],
      declarations: [UserSessionSignUpComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(UserSessionSignUpComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    usuarioService = TestBed.inject(SessionManager) as jasmine.SpyObj<SessionManager>;
    enumsService = TestBed.inject(EnumsService) as jasmine.SpyObj<EnumsService>;
  });

  beforeEach(() => {
    dummyUsuarios = [
      new UserSession(
        faker.lorem.word(),
        faker.lorem.word(),
        "admin"
      ),
    ];

    enumsService.bancos.and.returnValue(of(bancos));

    fixture.detectChanges();
    component.ngOnInit();
    component.onItemChange(1);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has 1 <input.form-control> with id name element", () => {
    expect(debug.queryAll(By.css('#nombre'))).toHaveSize(1);
  });

  it("Should see nombre-requerido label", () => {
    expect(debug.queryAll(By.css('#nombre-requerido'))).toHaveSize(0);
    component.finalForm.controls['nombre'].setValue('');
    component.finalForm.controls['nombre'].markAsTouched();

    const nombre = component.finalForm.controls['nombre'];
    expect(nombre.valid).toBeFalsy();

    fixture.detectChanges();
    expect(nombre.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#nombre')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#nombre-requerido'))).toHaveSize(1);
  });

  it("Should see tamano-nombre-excedido label", () => {
    const nameValue = faker.lorem.words(10)

    expect(debug.queryAll(By.css('#tamano-nombre-excedido'))).toHaveSize(0);
    component.finalForm.controls['nombre'].setValue(nameValue);
    component.finalForm.controls['nombre'].markAsTouched();

    const nombre = component.finalForm.controls['nombre'];

    expect(nombre.valid).toBeFalsy();

    fixture.detectChanges();
    expect(nombre.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#nombre')).nativeElement.value).toEqual(nameValue);
    expect(debug.queryAll(By.css('#tamano-nombre-excedido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id telefono element", () => {
    expect(debug.queryAll(By.css('#telefono'))).toHaveSize(1);
  });

  it("Should see telefono-requerido label", () => {
    expect(debug.queryAll(By.css('#telefono-requerido'))).toHaveSize(0);
    component.finalForm.controls['telefono'].setValue('');
    component.finalForm.controls['telefono'].markAsTouched();

    const telefono = component.finalForm.controls['telefono'];
    expect(telefono.valid).toBeFalsy();

    fixture.detectChanges();
    expect(telefono.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#telefono')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#telefono-requerido'))).toHaveSize(1);
  });

  it("Should see tamano-telfono-excedido label", () => {
    const telefonoValue = faker.number.bigInt().toString() + "00"

    expect(debug.queryAll(By.css('#tamano-telefono-excedido'))).toHaveSize(0);
    component.finalForm.controls['telefono'].setValue(telefonoValue);
    component.finalForm.controls['telefono'].markAsTouched();

    const telefono = component.finalForm.controls['telefono'];

    expect(telefono.valid).toBeFalsy();

    fixture.detectChanges();
    expect(telefono.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#telefono')).nativeElement.value).toEqual(telefonoValue);
    expect(debug.queryAll(By.css('#tamano-telefono-excedido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id banco element", () => {
    expect(debug.queryAll(By.css('#banco'))).toHaveSize(1);
  });

  it("Should see banco-requerido label", () => {
    expect(debug.queryAll(By.css('#banco-requerido'))).toHaveSize(0);
    component.finalForm.controls['banco'].setValue('');
    component.finalForm.controls['banco'].markAsTouched();

    const banco = component.finalForm.controls['banco'];
    expect(banco.valid).toBeFalsy();

    fixture.detectChanges();
    expect(banco.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#banco')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#banco-requerido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id cuenta element", () => {
    expect(debug.queryAll(By.css('#cuenta'))).toHaveSize(1);
  });

  it("Should see cuenta-requerida label", () => {
    expect(debug.queryAll(By.css('#cuenta-requerida'))).toHaveSize(0);
    component.finalForm.controls['cuenta'].setValue('');
    component.finalForm.controls['cuenta'].markAsTouched();

    const cuenta = component.finalForm.controls['cuenta'];
    expect(cuenta.valid).toBeFalsy();

    fixture.detectChanges();
    expect(cuenta.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#cuenta')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#cuenta-requerida'))).toHaveSize(1);
  });

  it("Should see tamano-cuenta-excedida label", () => {
    const cuentaValue = faker.number.bigInt().toString() + faker.number.bigInt().toString()

    expect(debug.queryAll(By.css('#tamano-cuenta-excedida'))).toHaveSize(0);
    component.finalForm.controls['cuenta'].setValue(cuentaValue);
    component.finalForm.controls['cuenta'].markAsTouched();

    const cuenta = component.finalForm.controls['cuenta'];

    expect(cuenta.valid).toBeFalsy();

    fixture.detectChanges();
    expect(cuenta.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#cuenta')).nativeElement.value).toEqual(cuentaValue);
    expect(debug.queryAll(By.css('#tamano-cuenta-excedida'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id correo element", () => {
    expect(debug.queryAll(By.css('#correo'))).toHaveSize(1);
  });

  it("Should see correo-requerido label", () => {
    expect(debug.queryAll(By.css('#correo-requerido'))).toHaveSize(0);
    component.finalForm.controls['correo'].setValue('');
    component.finalForm.controls['correo'].markAsTouched();

    const correo = component.finalForm.controls['correo'];
    expect(correo.valid).toBeFalsy();

    fixture.detectChanges();
    expect(correo.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#correo')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#correo-requerido'))).toHaveSize(1);
  });

  it("Should see correo-invalido label", () => {
    const correoValue = faker.lorem.word();

    expect(debug.queryAll(By.css('#correo-invalido'))).toHaveSize(0);
    component.finalForm.controls['correo'].setValue(correoValue);
    component.finalForm.controls['correo'].markAsTouched();

    const correo = component.finalForm.controls['correo'];
    expect(correo.valid).toBeFalsy();

    fixture.detectChanges();
    expect(correo.hasError('pattern')).toBeTruthy();
    expect(debug.query(By.css('#correo')).nativeElement.value).toEqual(correoValue);
    expect(debug.queryAll(By.css('#correo-invalido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id usuario element", () => {
    expect(debug.queryAll(By.css('#usuario'))).toHaveSize(1);
  });

  it("Should see usuario-requerido label", () => {
    expect(debug.queryAll(By.css('#usuario-requerido'))).toHaveSize(0);
    component.finalForm.controls['usuario'].setValue('');
    component.finalForm.controls['usuario'].markAsTouched();

    const usuario = component.finalForm.controls['usuario'];
    expect(usuario.valid).toBeFalsy();

    fixture.detectChanges();
    expect(usuario.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#usuario')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#usuario-requerido'))).toHaveSize(1);
  });

  it("Should see tamano-usuario-excedido label", () => {
    const usuarioValue = faker.lorem.words(10)

    expect(debug.queryAll(By.css('#tamano-usuario-excedido'))).toHaveSize(0);
    component.finalForm.controls['usuario'].setValue(usuarioValue);
    component.finalForm.controls['usuario'].markAsTouched();

    const usuario = component.finalForm.controls['usuario'];

    expect(usuario.valid).toBeFalsy();

    fixture.detectChanges();
    expect(usuario.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#usuario')).nativeElement.value).toEqual(usuarioValue);
    expect(debug.queryAll(By.css('#tamano-usuario-excedido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id contrasena element", () => {
    expect(debug.queryAll(By.css('#contrasena'))).toHaveSize(1);
  });

  it("Should see contrasena-requerida label", () => {
    expect(debug.queryAll(By.css('#contrasena-requerida'))).toHaveSize(0);
    component.finalForm.controls['contrasena'].setValue('');
    component.finalForm.controls['contrasena'].markAsTouched();

    const contrasena = component.finalForm.controls['contrasena'];
    expect(contrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(contrasena.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#contrasena')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#contrasena-requerida'))).toHaveSize(1);
  });

  it("Should see tamano-contrasena-excedido label", () => {
    const contrasenaValue = faker.lorem.words(10)

    expect(debug.queryAll(By.css('#tamano-contrasena-excedido'))).toHaveSize(0);
    component.finalForm.controls['contrasena'].setValue(contrasenaValue);
    component.finalForm.controls['contrasena'].markAsTouched();

    const contrasena = component.finalForm.controls['contrasena'];

    expect(contrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(contrasena.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#contrasena')).nativeElement.value).toEqual(contrasenaValue);
    expect(debug.queryAll(By.css('#tamano-contrasena-excedido'))).toHaveSize(1);
  });

  it("Should see tamano-contrasena-minimo-requerido label", () => {
    const contrasenaValue = faker.lorem.word(1)

    expect(debug.queryAll(By.css('#tamano-contrasena-minimo-requerido'))).toHaveSize(0);
    component.finalForm.controls['contrasena'].setValue(contrasenaValue);
    component.finalForm.controls['contrasena'].markAsTouched();

    const contrasena = component.finalForm.controls['contrasena'];

    expect(contrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(contrasena.hasError('minlength')).toBeTruthy();
    expect(debug.query(By.css('#contrasena')).nativeElement.value).toEqual(contrasenaValue);
    expect(debug.queryAll(By.css('#tamano-contrasena-minimo-requerido'))).toHaveSize(1);
  });

  it("Component has 1 <input.form-control> with id confirmar-contrasena element", () => {
    expect(debug.queryAll(By.css('#confirmar-contrasena'))).toHaveSize(1);
  });

  it("Should see confirmar-contrasena-requerida label", () => {
    expect(debug.queryAll(By.css('#confirmar-contrasena-requerida'))).toHaveSize(0);
    component.finalForm.controls['confirmarContrasena'].setValue('');
    component.finalForm.controls['confirmarContrasena'].markAsTouched();

    const confirmarContrasena = component.finalForm.controls['confirmarContrasena'];
    expect(confirmarContrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(confirmarContrasena.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#confirmar-contrasena')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#confirmar-contrasena-requerida'))).toHaveSize(1);
  });

  it("Should see tamano-confirmar-contrasena-excedido label", () => {
    const confirmarContrasenaValue = faker.lorem.words(10)

    expect(debug.queryAll(By.css('#tamano-confirmar-contrasena-excedido'))).toHaveSize(0);
    component.finalForm.controls['confirmarContrasena'].setValue(confirmarContrasenaValue);
    component.finalForm.controls['confirmarContrasena'].markAsTouched();

    const confirmarContrasena = component.finalForm.controls['confirmarContrasena'];

    expect(confirmarContrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(confirmarContrasena.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#confirmar-contrasena')).nativeElement.value).toEqual(confirmarContrasenaValue);
    expect(debug.queryAll(By.css('#tamano-confirmar-contrasena-excedido'))).toHaveSize(1);
  });

  it("Should see tamano-confirmar-contrasena-minimo-requerido label", () => {
    const confirmarContrasenaValue = faker.lorem.word(1)

    expect(debug.queryAll(By.css('#tamano-confirmar-contrasena-minimo-requerid'))).toHaveSize(0);
    component.finalForm.controls['confirmarContrasena'].setValue(confirmarContrasenaValue);
    component.finalForm.controls['confirmarContrasena'].markAsTouched();

    const contrasena = component.finalForm.controls['confirmarContrasena'];

    expect(contrasena.valid).toBeFalsy();

    fixture.detectChanges();
    expect(contrasena.hasError('minlength')).toBeTruthy();
    expect(debug.query(By.css('#confirmar-contrasena')).nativeElement.value).toEqual(confirmarContrasenaValue);
    expect(debug.queryAll(By.css('#tamano-confirmar-contrasena-minimo-requerido'))).toHaveSize(1);
  });

  it("Should see contrasena-no-coincide label", () => {
    const contrasenaValue = faker.lorem.word(5)
    const confirmarContrasenaValue = faker.lorem.word(5)

    expect(debug.queryAll(By.css('#contrasena-no-coincide'))).toHaveSize(0);
    component.finalForm.controls['contrasena'].setValue(contrasenaValue);
    component.finalForm.controls['confirmarContrasena'].setValue(confirmarContrasenaValue);
    component.finalForm.controls['contrasena'].markAsTouched();
    component.finalForm.controls['confirmarContrasena'].markAsTouched();

    const contrasena = component.finalForm.controls['contrasena'];
    const confirmarContrasena = component.finalForm.controls['confirmarContrasena'];

    expect(contrasena.valid).toBeTruthy();
    expect(confirmarContrasena.valid).toBeTruthy();

    fixture.detectChanges();
    expect(debug.query(By.css('#contrasena')).nativeElement.value).toEqual(contrasenaValue);
    expect(debug.query(By.css('#confirmar-contrasena')).nativeElement.value).toEqual(confirmarContrasenaValue);
    expect(debug.queryAll(By.css('#contrasena-no-coincide'))).toHaveSize(1);
  });

  it("Component has 1 <button.btn.btn-info.col-8>  for signin usuario", () => {
    expect(debug.queryAll(By.css('button.btn.btn-info.col-8'))).toHaveSize(1);
  });
});