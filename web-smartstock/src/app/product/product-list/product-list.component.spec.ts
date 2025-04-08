/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { fa, faker } from '@faker-js/faker';

import { ProductListComponent } from './product-list.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule } from 'ngx-toastr';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { of } from 'rxjs';

import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { Product } from '../product';

describe('ProductEditComponent', () => {
  let component: ProductListComponent;
  let fixture: ComponentFixture<ProductListComponent>;
  let debug: DebugElement;

  let productService: jasmine.SpyObj<ProductService>;

  beforeEach(async(() => {
    const productServiceSpy = jasmine.createSpyObj('ProductService', ['getProducts']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        TranslateModule.forRoot(),
        ReactiveFormsModule
      ],
      providers: [
        { provide: ProductService, useValue: productServiceSpy },
        FormBuilder,
        TranslateService
      ],
      declarations: [ ProductListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProductListComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    productService = TestBed.inject(ProductService) as jasmine.SpyObj<ProductService>;
  }));

  beforeEach(() => {
    productService.getProducts.and.returnValue(of([
      new Product( 
        faker.string.uuid(),
        faker.string.uuid(),
        faker.lorem.word(),
        faker.lorem.word(),
        'ELECTRONIC',
        faker.number.int({ min: 1, max: 10 }),
        'EUR',
        false,
        0,
        null,
        faker.image.url(),
        faker.lorem.word()
      ),
      new Product( 
        faker.string.uuid(),
        faker.string.uuid(),
        faker.lorem.word(),
        faker.lorem.word(),
        'ELECTRONIC',
        faker.number.int({ min: 1, max: 10 }),
        'EUR',
        false,
        0,
        null,
        faker.image.url(),
        faker.lorem.word()
      )]));

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has a title", () => {
    let title = debug.query(By.css('h4')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it("Component has an table product_list_table", () => {
    expect(debug.queryAll(By.css('#product_list_table'))).toHaveSize(1);
  });

  it("Component has a table with 2 rows", () => {
    let rows = debug.queryAll(By.css('#product_list_table tbody tr'));
    expect(rows).toHaveSize(2);

    debug.queryAll(By.css('#product_list_table tbody tr')).forEach((row, index) => {
      let product = component.products[index];
      let cells = row.queryAll(By.css('td'));
      expect(cells[0].nativeElement.innerHTML).toBe(product.id);
      expect(cells[1].nativeElement.innerHTML).toBe(product.name);
      expect(cells[2].nativeElement.innerHTML).toBe(product.description);
      expect(cells[3].nativeElement.innerHTML).toBe(product.unit_price.toString());
      expect(cells[4].nativeElement.innerHTML).toBe(product.currency_price);
    });
  });
});