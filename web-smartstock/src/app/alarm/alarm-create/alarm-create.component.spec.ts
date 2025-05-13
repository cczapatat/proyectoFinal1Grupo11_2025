/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { faker } from '@faker-js/faker';

import { AlarmCreateComponent } from './alarm-create.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule } from 'ngx-toastr';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { ManufacturerService } from '../../services/manufacturer.service';
import { of } from 'rxjs';
import { Manufacturer } from '../../dtos/manufacturer';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { Product } from '../../product/product';

describe('ProductCreateComponent', () => {
  let component: AlarmCreateComponent;
  let fixture: ComponentFixture<AlarmCreateComponent>;
  let debug: DebugElement;

  let manufacturerService: jasmine.SpyObj<ManufacturerService>;
  let productService: jasmine.SpyObj<ProductService>;

  beforeEach(async(() => {
    const manufacturerServiceSpy = jasmine.createSpyObj('ManufacturerService', ['getManufacturerList']);
    const productServiceSpy = jasmine.createSpyObj('ProductService', ['getProductsByManufactureId']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        TranslateModule.forRoot(),
        ReactiveFormsModule
      ],
      providers: [
        { provide: ManufacturerService, useValue: manufacturerServiceSpy },
        { provide: ProductService, useValue: productServiceSpy },
        FormBuilder,
        TranslateService
      ],
      declarations: [ AlarmCreateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlarmCreateComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    manufacturerService = TestBed.inject(ManufacturerService) as jasmine.SpyObj<ManufacturerService>;
    productService = TestBed.inject(ProductService) as jasmine.SpyObj<ProductService>;
  }));

  beforeEach(() => {
    manufacturerService.getManufacturerList.and.returnValue(of([
      new Manufacturer(
        faker.string.uuid(),
        faker.company.name(),
        faker.location.streetAddress(),
        faker.phone.number(),
        faker.internet.email(),
        faker.location.country(),
        faker.lorem.sentence(),
        faker.lorem.sentence(),
        5
      ),
    ]));

    productService.getProductsByManufactureId.and.returnValue(of([
      new Product(
        faker.string.uuid(),
        faker.string.uuid(),
        faker.commerce.productName(),
        faker.lorem.sentence(),
        faker.commerce.department(),
        faker.number.float({ min: 1, max: 500 }),
        'USD',
        false,
        null,
        null,
        faker.image.imageUrl(),
        faker.lorem.sentence(),
        faker.number.float({ min: 1, max: 500 })
      ),
    ]));

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has a title", () => {
    let title = debug.query(By.css('h1')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it("Component has a manufacture_id select option", () => {
    const selectElement = debug.query(By.css('#manufacture_id')).nativeElement;
    expect(selectElement).toBeTruthy();
    const options = selectElement.querySelectorAll('option');
    expect(options.length).toBe(2);
  });

  it("Component has a product_id select option", () => {
    const manufactureSelectElement = debug.query(By.css('#manufacture_id')).nativeElement;
    manufactureSelectElement.value = manufactureSelectElement.options[1].value; // Select the first option (index 1)
    manufactureSelectElement.dispatchEvent(new Event('change')); // Trigger change event

    fixture.detectChanges();

    const productSelectElement = debug.query(By.css('#product_id')).nativeElement;
    expect(productSelectElement).toBeTruthy();
    const options = productSelectElement.querySelectorAll('option');
    expect(options.length).toBe(2); 
  });

  it("Component has an input is_set_min_value", () => {
    expect(debug.queryAll(By.css('#is_set_min_value'))).toHaveSize(1);
  });

  it("Component has an input is_set_max_value", () => {
    expect(debug.queryAll(By.css('#is_set_max_value'))).toHaveSize(1);
  });

  it("Component has an input minimum_value", () => {
    expect(debug.queryAll(By.css('#minimum_value'))).toHaveSize(1);
  });

  it("Should see alarm_min_value_required label", () => {
    expect(debug.queryAll(By.css('#alarm_min_value_required'))).toHaveSize(0);
    component.alarmForm.controls['minimum_value'].enable();
    component.alarmForm.controls['minimum_value'].setValue('');
    component.alarmForm.controls['minimum_value'].markAsTouched();

    const minimum_value = component.alarmForm.controls['minimum_value'];
    expect(minimum_value.valid).toBeFalsy();

    fixture.detectChanges();
    expect(minimum_value.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#minimum_value')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#alarm_min_value_required'))).toHaveSize(1);
  });

  it("Should see alarm_min_value_invalid label", () => {
    expect(debug.queryAll(By.css('#alarm_min_value_invalid'))).toHaveSize(0);
    component.alarmForm.controls['minimum_value'].enable();
    component.alarmForm.controls['minimum_value'].setValue('-100');
    component.alarmForm.controls['minimum_value'].markAsTouched();

    const minimum_value = component.alarmForm.controls['minimum_value'];
    expect(minimum_value.valid).toBeFalsy();

    fixture.detectChanges();
    expect(minimum_value.hasError('min')).toBeTruthy();
    expect(debug.query(By.css('#minimum_value')).nativeElement.value).toEqual('-100');
    expect(debug.queryAll(By.css('#alarm_min_value_invalid'))).toHaveSize(1);
  });

  it("Should see alarm_max_value_required label", () => {
    expect(debug.queryAll(By.css('#alarm_max_value_required'))).toHaveSize(0);
    component.alarmForm.controls['maximum_value'].enable();
    component.alarmForm.controls['maximum_value'].setValue('');
    component.alarmForm.controls['maximum_value'].markAsTouched();

    const maximum_value = component.alarmForm.controls['maximum_value'];
    expect(maximum_value.valid).toBeFalsy();

    fixture.detectChanges();
    expect(maximum_value.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#maximum_value')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#alarm_max_value_required'))).toHaveSize(1);
  });

  it("Should see alarm_max_value_invalid label", () => {
    expect(debug.queryAll(By.css('#alarm_max_value_invalid'))).toHaveSize(0);
    component.alarmForm.controls['maximum_value'].enable();
    component.alarmForm.controls['maximum_value'].setValue('-100');
    component.alarmForm.controls['maximum_value'].markAsTouched();

    const maximum_value = component.alarmForm.controls['maximum_value'];
    expect(maximum_value.valid).toBeFalsy();

    fixture.detectChanges();
    expect(maximum_value.hasError('notPositive')).toBeTruthy();
    expect(debug.query(By.css('#maximum_value')).nativeElement.value).toEqual('-100');
    expect(debug.queryAll(By.css('#alarm_max_value_invalid'))).toHaveSize(1);
  });

  it("Component has an input notes", () => {
    expect(debug.queryAll(By.css('#notes'))).toHaveSize(1);
  });

  it("Should see alarm_notes_required label", () => {
    expect(debug.queryAll(By.css('#alarm_notes_required'))).toHaveSize(0);
    component.alarmForm.controls['notes'].setValue('');
    component.alarmForm.controls['notes'].markAsTouched();

    const notes = component.alarmForm.controls['notes'];
    expect(notes.valid).toBeFalsy();

    fixture.detectChanges();
    expect(notes.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#notes')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#alarm_notes_required'))).toHaveSize(1);
  });

  it("Component has a button", () => {
    let title = debug.query(By.css('button')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it('should contain a form element', () => {
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('form')).toBeTruthy();
  });

  it('should have valid form', () => {
    const form = component.alarmForm;
      fixture.detectChanges();
    form.controls['manufacture_id'].setValue("1");
    form.controls['product_id'].setValue("1");
    form.controls['is_set_min_value'].setValue(true);
    form.controls['is_set_max_value'].setValue(true);
    form.controls['minimum_value'].setValue("1");
    form.controls['maximum_value'].setValue("100");
    form.controls['notes'].setValue("notes");
    expect(form.invalid).toBeFalsy();
  });

  it('should have invalid form', () => {
    const form = component.alarmForm;
    fixture.detectChanges();
    form.controls['manufacture_id'].setValue("1");
    form.controls['product_id'].setValue("1");
    form.controls['is_set_min_value'].setValue(true);
    form.controls['is_set_max_value'].setValue(true);
    form.controls['minimum_value'].setValue("");
    form.controls['maximum_value'].setValue("100");
    form.controls['notes'].setValue("notes");
    expect(form.invalid).toBeTruthy();
  });

  it('should build alarm payload with minimum and maximum values', () => {
    const formValues = {
      manufacture_id: '1',
      product_id: '2',
      notes: 'Test notes',
      is_set_min_value: true,
      is_set_max_value: true,
      minimum_value: 10,
      maximum_value: 100
    };
  
    const payload = component['buildAlarmPayload'](formValues);
  
    expect(payload).toEqual({
      manufacture_id: '1',
      product_id: '2',
      notes: 'Test notes',
      minimum_value: 10,
      maximum_value: 100
    });
  });
});
