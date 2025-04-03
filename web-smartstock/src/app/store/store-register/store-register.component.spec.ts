import { DebugElement } from "@angular/core";
import { async, ComponentFixture, TestBed } from "@angular/core/testing";
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { StoreService } from "src/app/services/store.service";
import { StoreRegisterComponent } from "./store-register.component";
import { RouterTestingModule } from "@angular/router/testing";
import { ToastrModule } from "ngx-toastr";
import { FormBuilder, ReactiveFormsModule } from "@angular/forms";
import { TranslateModule, TranslateService } from "@ngx-translate/core";
import { of, throwError } from "rxjs";
import { StoreDto } from "src/app/dtos/store.dto";
import { By } from "@angular/platform-browser";

describe('StoreRegisterComponent', () => {
  let component: StoreRegisterComponent;
  let fixture: ComponentFixture<StoreRegisterComponent>;
  let debug: DebugElement;
  let storeService: jasmine.SpyObj<StoreService>;

  beforeEach(async () => {
    const storeServiceSpy = jasmine.createSpyObj('StoreService', ['getStates', 'getSecurityLevels', 'registerStore']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ReactiveFormsModule,
        TranslateModule.forRoot(),
        ToastrModule.forRoot(),
      ],
      providers: [
        FormBuilder,
        TranslateService,
        { provide: StoreService, useValue: storeServiceSpy },
      ],
      declarations: [StoreRegisterComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(StoreRegisterComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    storeService = TestBed.inject(StoreService) as jasmine.SpyObj<StoreService>;
  });

  beforeEach(() => {
    storeService.getStates.and.returnValue(of(['ACTIVE', 'INACTIVE']));
    storeService.getSecurityLevels.and.returnValue(of(['HIGH', 'MEDIUM', 'LOW']));
    storeService.registerStore.and.returnValue(of(new StoreDto(
      'storeName',
      'storePhone',
      'storeEmail',
      'storeAddress',
      100,
      'ACTIVE',
      'HIGH',
      'uuid',
      new Date(),
      new Date(),
    )));

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has a title", () => {
    let title = debug.query(By.css('h2')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it("Component has a minimum items", () => {
    expect(debug.queryAll(By.css('#store_name'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_name_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_phone'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_phone_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_email'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_email_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_address'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_address_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_capacity'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_capacity_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_state'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_state_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_security_level'))).toHaveSize(1);
    expect(debug.queryAll(By.css('#store_security_level_error'))).toHaveSize(0);
    expect(debug.queryAll(By.css('#store_btn_register'))).toHaveSize(1);
  });

  it("Component has a error about store_name", () => {
    expect(debug.queryAll(By.css('#store_name_error'))).toHaveSize(0);
    component.storeForm.controls['name'].setValue('');
    component.storeForm.controls['name'].markAsTouched();

    const name = component.storeForm.controls['name'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_name')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_name_error'))).toHaveSize(1);
  });

  it("Component has a error about store_phone", () => {
    expect(debug.queryAll(By.css('#store_phone_error'))).toHaveSize(0);
    component.storeForm.controls['phone'].setValue('');
    component.storeForm.controls['phone'].markAsTouched();

    const name = component.storeForm.controls['phone'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_phone')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_phone_error'))).toHaveSize(1);
  });

  it("Component has a error about store_email", () => {
    expect(debug.queryAll(By.css('#store_email_error'))).toHaveSize(0);
    component.storeForm.controls['email'].setValue('');
    component.storeForm.controls['email'].markAsTouched();

    const name = component.storeForm.controls['email'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_email')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_email_error'))).toHaveSize(1);
  });

  it("Component has a error about store_address", () => {
    expect(debug.queryAll(By.css('#store_address_error'))).toHaveSize(0);
    component.storeForm.controls['address'].setValue('');
    component.storeForm.controls['address'].markAsTouched();

    const name = component.storeForm.controls['address'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_address')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_address_error'))).toHaveSize(1);
  });

  it("Component has a error about store_capacity", () => {
    expect(debug.queryAll(By.css('#store_capacity_error'))).toHaveSize(0);
    component.storeForm.controls['capacity'].setValue('');
    component.storeForm.controls['capacity'].markAsTouched();

    const name = component.storeForm.controls['capacity'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_capacity')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_capacity_error'))).toHaveSize(1);
  });

  it("Component has a error about store_state", () => {
    expect(debug.queryAll(By.css('#store_state_error'))).toHaveSize(0);
    component.storeForm.controls['state'].setValue('');
    component.storeForm.controls['state'].markAsTouched();

    const name = component.storeForm.controls['state'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_state')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_state_error'))).toHaveSize(1);
  });

  it("Component has a error about store_security_level", () => {
    expect(debug.queryAll(By.css('#store_security_level_error'))).toHaveSize(0);
    component.storeForm.controls['securityLevel'].setValue('');
    component.storeForm.controls['securityLevel'].markAsTouched();

    const name = component.storeForm.controls['securityLevel'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_security_level')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#store_security_level_error'))).toHaveSize(1);
  });

  it("Component has a state select option", () => {
    const selectElement = debug.query(By.css('#store_state')).nativeElement;
    expect(selectElement).toBeTruthy();
    const options = selectElement.querySelectorAll('option');
    expect(options.length).toBe(3);
  });

  it("Component has a security level select option", () => {
    const selectElement = debug.query(By.css('#store_security_level')).nativeElement;
    expect(selectElement).toBeTruthy();
    const options = selectElement.querySelectorAll('option');
    expect(options.length).toBe(4);
  });

  it("Component action to submit button - success", () => {
    const submitButton = debug.query(By.css('#store_btn_register')).nativeElement;
    expect(submitButton).toBeTruthy();

    const form = component.storeForm;
    fixture.detectChanges();

    expect(form.valid).toBeFalsy();
    component.storeForm.controls['name'].setValue('Test Store');
    component.storeForm.controls['phone'].setValue('12345678901');
    component.storeForm.controls['email'].setValue('test@test.com');
    component.storeForm.controls['address'].setValue('Test Address');
    component.storeForm.controls['capacity'].setValue(100);
    component.storeForm.controls['state'].setValue('ACTIVE');
    component.storeForm.controls['securityLevel'].setValue('HIGH');
    fixture.detectChanges();
    expect(form.valid).toBeTruthy();
    expect(debug.query(By.css('#store_btn_register')).nativeElement.disabled).toBeFalsy();

    const button = debug.query(By.css('#store_btn_register'));
    button.nativeElement.click();

    fixture.detectChanges();
    expect(storeService.registerStore).toHaveBeenCalled();
    expect(storeService.registerStore.calls.count()).toBe(1);
    expect(storeService.registerStore.calls.argsFor(0)[0]).toEqual(new StoreDto(
      'Test Store',
      '12345678901',
      'test@test.com',
      'Test Address',
      100,
      'ACTIVE',
      'HIGH',
    ));
    expect(debug.query(By.css('#store_btn_register')).nativeElement.disabled).toBeTruthy();
  });

  it("Component action to submit button - empty", () => {
    const submitButton = debug.query(By.css('#store_btn_register')).nativeElement;
    expect(submitButton).toBeTruthy();

    const form = component.storeForm;
    fixture.detectChanges();

    expect(form.valid).toBeFalsy();
    component.storeForm.controls['name'].setValue('');
    component.storeForm.controls['phone'].setValue('');
    component.storeForm.controls['email'].setValue('');
    component.storeForm.controls['address'].setValue('');
    component.storeForm.controls['capacity'].setValue('');
    component.storeForm.controls['state'].setValue('');
    component.storeForm.controls['securityLevel'].setValue('');
    fixture.detectChanges();
    expect(form.valid).toBeFalsy();
    expect(debug.query(By.css('#store_btn_register')).nativeElement.disabled).toBeTruthy();

    const button = debug.query(By.css('#store_btn_register'));
    button.nativeElement.click();

    fixture.detectChanges();
    expect(storeService.registerStore.calls.count()).toBe(0);
  });

  it("Component action to submit button - service error", () => {
    storeService.registerStore.and.returnValue(throwError(() => new Error('Service failed')));
    
    const submitButton = debug.query(By.css('#store_btn_register')).nativeElement;
    expect(submitButton).toBeTruthy();

    const form = component.storeForm;
    fixture.detectChanges();

    component.storeForm.controls['name'].setValue('Test Store');
    component.storeForm.controls['phone'].setValue('12345678901');
    component.storeForm.controls['email'].setValue('test@test.com');
    component.storeForm.controls['address'].setValue('Test Address');
    component.storeForm.controls['capacity'].setValue(100);
    component.storeForm.controls['state'].setValue('ACTIVE');
    component.storeForm.controls['securityLevel'].setValue('HIGH');
    fixture.detectChanges();
    
    expect(form.valid).toBeTruthy();
    expect(debug.query(By.css('#store_btn_register')).nativeElement.disabled).toBeFalsy();

    const button = debug.query(By.css('#store_btn_register'));
    button.nativeElement.click();

    fixture.detectChanges();
    expect(storeService.registerStore).toHaveBeenCalled();
    expect(storeService.registerStore.calls.count()).toBe(1);
    expect(form.valid).toBeTruthy();
    expect(debug.query(By.css('#store_btn_register')).nativeElement.disabled).toBeFalsy();
  });
});
