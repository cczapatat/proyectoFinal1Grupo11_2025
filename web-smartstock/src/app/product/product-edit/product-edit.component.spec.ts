/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { fa, faker, fi } from '@faker-js/faker';

import { ProductEditComponent } from './product-edit.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule } from 'ngx-toastr';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { ManufacturerService } from '../../services/manufacturer.service';
import { of } from 'rxjs';

import { ProductCurrency } from '../../dtos/product-currency';
import { ProductCategory } from '../../dtos/product-category';
import { Manufacturer } from '../../dtos/manufacturer';
import { TranslateModule, TranslateService } from '@ngx-translate/core';

describe('ProductEditComponent', () => {
  let component: ProductEditComponent;
  let fixture: ComponentFixture<ProductEditComponent>;
  let debug: DebugElement;

  let manufacturerService: jasmine.SpyObj<ManufacturerService>;
  let productService: jasmine.SpyObj<ProductService>;

  beforeEach(async(() => {
    const manufacturerServiceSpy = jasmine.createSpyObj('ManufacturerService', ['getManufacturerList']);
    const productServiceSpy = jasmine.createSpyObj('ProductService', ['createProduct', 'getProductCategories', 'getProductCurrencies']);

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
      declarations: [ ProductEditComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProductEditComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    manufacturerService = TestBed.inject(ManufacturerService) as jasmine.SpyObj<ManufacturerService>;
    productService = TestBed.inject(ProductService) as jasmine.SpyObj<ProductService>;
  }));

  beforeEach(() => {
    productService.getProductCategories.and.returnValue(of([new ProductCategory('ELECTRONIC', 'ELECTRONIC')]));
    productService.getProductCurrencies.and.returnValue(of([new ProductCurrency('EUR', 'EUR'), new ProductCurrency('COP', 'COP')]));
    manufacturerService.getManufacturerList.and.returnValue(of([
      new Manufacturer(
        '1',
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

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has a title", () => {
    let title = debug.query(By.css('h4')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it("Component has an input product_name", () => {
    expect(debug.queryAll(By.css('#product_name'))).toHaveSize(1);
  });

  it("Should see product_name_required label", () => {
    expect(debug.queryAll(By.css('#product_name_required'))).toHaveSize(0);
    component.productForm.controls['name'].setValue('');
    component.productForm.controls['name'].markAsTouched();

    const name = component.productForm.controls['name'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#product_name')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#product_name_required'))).toHaveSize(1);
  });

  it("Should see product_name_exceed label", () => {
    const nameValue = faker.lorem.words(100);
    expect(debug.queryAll(By.css('#product_name_exceed'))).toHaveSize(0);
    component.productForm.controls['name'].setValue(nameValue);
    component.productForm.controls['name'].markAsTouched();

    const name = component.productForm.controls['name'];
    expect(name.valid).toBeFalsy();

    fixture.detectChanges();
    expect(name.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#product_name')).nativeElement.value).toEqual(nameValue);
    expect(debug.queryAll(By.css('#product_name_exceed'))).toHaveSize(1);
  });

  it("Component has an input description", () => {
    let title = debug.query(By.css('h4')).nativeElement;
    expect(debug.queryAll(By.css('#description'))).toHaveSize(1);
  });

  it("Should see product_description_required label", () => {
    expect(debug.queryAll(By.css('#product_description_required'))).toHaveSize(0);
    component.productForm.controls['description'].setValue('');
    component.productForm.controls['description'].markAsTouched();

    const description = component.productForm.controls['description'];
    expect(description.valid).toBeFalsy();

    fixture.detectChanges();
    expect(description.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#description')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#product_description_required'))).toHaveSize(1);
  });

  it("Should see product_description_exceed label", () => {
    const descriptionValue = faker.lorem.words(100);
    expect(debug.queryAll(By.css('#product_description_exceed'))).toHaveSize(0);
    component.productForm.controls['description'].setValue(descriptionValue);
    component.productForm.controls['description'].markAsTouched();

    const description = component.productForm.controls['description'];
    expect(description.valid).toBeFalsy();

    fixture.detectChanges();
    expect(description.hasError('maxlength')).toBeTruthy();
    expect(debug.query(By.css('#description')).nativeElement.value).toEqual(descriptionValue);
    expect(debug.queryAll(By.css('#product_description_exceed'))).toHaveSize(1);
  });

  it("Component has a category select option", () => {
    const selectElement = debug.query(By.css('#category')).nativeElement;
    expect(selectElement).toBeTruthy();
    const options = selectElement.querySelectorAll('option');
    expect(options.length).toBe(2);
  });

  it("Component has a manufacturer select option", () => {
    const selectElement = debug.query(By.css('#manufacturer')).nativeElement;
    expect(selectElement).toBeTruthy();
    const options = selectElement.querySelectorAll('option');
    expect(options.length).toBe(2);
  });

  it("Component has an input unit_price", () => {
    expect(debug.queryAll(By.css('#unit_price'))).toHaveSize(1);
  });

  it("Should see product_unit_price_required label", () => {
    expect(debug.queryAll(By.css('#product_unit_price_required'))).toHaveSize(0);
    component.productForm.controls['unit_price'].setValue('');
    component.productForm.controls['unit_price'].markAsTouched();

    const unit_price = component.productForm.controls['unit_price'];
    expect(unit_price.valid).toBeFalsy();

    fixture.detectChanges();
    expect(unit_price.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#unit_price')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#product_unit_price_required'))).toHaveSize(1);
  });

  it("Should see product_unit_price_invalid label", () => {
    expect(debug.queryAll(By.css('#product_unit_price_invalid'))).toHaveSize(0);
    component.productForm.controls['unit_price'].setValue('-100');
    component.productForm.controls['unit_price'].markAsTouched();

    const unit_price = component.productForm.controls['unit_price'];
    expect(unit_price.valid).toBeFalsy();

    fixture.detectChanges();
    expect(unit_price.hasError('notPositive')).toBeTruthy();
    expect(debug.query(By.css('#unit_price')).nativeElement.value).toEqual('-100');
    expect(debug.queryAll(By.css('#product_unit_price_invalid'))).toHaveSize(1);
  });

  it("Component has a currency select option", () => {
    const selectElement = debug.query(By.css('#currency')).nativeElement;
    expect(selectElement).toBeTruthy();
    const options = selectElement.querySelectorAll('option');
    expect(options.length).toBe(3);
  });

  it("Component has an input is_promotion", () => {
    expect(debug.queryAll(By.css('#is_promotion'))).toHaveSize(1);
  });

  it("Component has an input discount_price", () => {
    expect(debug.queryAll(By.css('#discount_price'))).toHaveSize(1);
  });

  it("Should see product_discount_price_required label", () => {
    expect(debug.queryAll(By.css('#product_discount_price_required'))).toHaveSize(0);
    component.productForm.controls['discount_price'].enable();
    component.productForm.controls['discount_price'].setValue('');
    component.productForm.controls['discount_price'].markAsTouched();

    const discount_price = component.productForm.controls['discount_price'];
    expect(discount_price.valid).toBeFalsy();

    fixture.detectChanges();
    expect(discount_price.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#discount_price')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#product_discount_price_required'))).toHaveSize(1);
  });

  it("Should see product_discount_price_invalid label", () => {
    expect(debug.queryAll(By.css('#product_discount_price_invalid'))).toHaveSize(0);
    component.productForm.controls['discount_price'].enable();
    component.productForm.controls['discount_price'].setValue('-100');
    component.productForm.controls['discount_price'].markAsTouched();

    const discount_price = component.productForm.controls['discount_price'];
    expect(discount_price.valid).toBeFalsy();

    fixture.detectChanges();
    expect(discount_price.hasError('notPositive')).toBeTruthy();
    expect(debug.query(By.css('#discount_price')).nativeElement.value).toEqual('-100');
    expect(debug.queryAll(By.css('#product_discount_price_invalid'))).toHaveSize(1);
  });

  it("Component has an input expired_at", () => {
    expect(debug.queryAll(By.css('#expired_at'))).toHaveSize(1);
  });

  it("Component has an input url_photo", () => {
    expect(debug.queryAll(By.css('#expired_at'))).toHaveSize(1);
  });

  it("Should see product_url_photo_required label", () => {
    expect(debug.queryAll(By.css('#product_url_photo_required'))).toHaveSize(0);
    component.productForm.controls['url_photo'].setValue('');
    component.productForm.controls['url_photo'].markAsTouched();

    const url_photo = component.productForm.controls['url_photo'];
    expect(url_photo.valid).toBeFalsy();

    fixture.detectChanges();
    expect(url_photo.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#url_photo')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#product_url_photo_required'))).toHaveSize(1);
  });

  it("Should see product_url_photo_invalid label", () => {
    expect(debug.queryAll(By.css('#product_url_photo_invalid'))).toHaveSize(0);
    component.productForm.controls['url_photo'].setValue('bad_url');
    component.productForm.controls['url_photo'].markAsTouched();

    const url_photo = component.productForm.controls['url_photo'];
    expect(url_photo.valid).toBeFalsy();

    fixture.detectChanges();
    expect(url_photo.hasError('pattern')).toBeTruthy();
    expect(debug.query(By.css('#url_photo')).nativeElement.value).toEqual('bad_url');
    expect(debug.queryAll(By.css('#product_url_photo_invalid'))).toHaveSize(1);
  });

  it("Component has an input store_conditions", () => {
    expect(debug.queryAll(By.css('#store_conditions'))).toHaveSize(1);
  });

  it("Should see product_store_conditions_required label", () => {
    expect(debug.queryAll(By.css('#product_store_conditions_required'))).toHaveSize(0);
    component.productForm.controls['store_conditions'].setValue('');
    component.productForm.controls['store_conditions'].markAsTouched();

    const store_conditions = component.productForm.controls['store_conditions'];
    expect(store_conditions.valid).toBeFalsy();

    fixture.detectChanges();
    expect(store_conditions.hasError('required')).toBeTruthy();
    expect(debug.query(By.css('#store_conditions')).nativeElement.value).toEqual('');
    expect(debug.queryAll(By.css('#product_store_conditions_required'))).toHaveSize(1);
  });

  it('should contain a form element', () => {
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('form')).toBeTruthy();
  });

  it('should have valid form', () => {
    const form = component.productForm;
      fixture.detectChanges();
    form.controls['manufacturer_id'].setValue("1");
    form.controls['name'].setValue("name");
    form.controls['description'].setValue("description");
    form.controls['category'].setValue("ELECTRONIC");
    form.controls['unit_price'].setValue("100");
    form.controls['currency_price'].setValue("EUR");
    form.controls['is_promotion'].setValue(false);
    form.controls['discount_price'].setValue("");
    form.controls['expired_at'].setValue(null);
    form.controls['url_photo'].setValue("https://example.com/photo.jpg");
    form.controls['store_conditions'].setValue("store_conditions");
    expect(form.invalid).toBeFalsy();
  });
});
