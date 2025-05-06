import { HttpClientTestingModule } from "@angular/common/http/testing";
import { DebugElement } from "@angular/core";
import { ComponentFixture, TestBed, fakeAsync, tick } from "@angular/core/testing";
import { ReactiveFormsModule, FormsModule } from "@angular/forms";
import { By } from "@angular/platform-browser";
import { TranslateModule, TranslateService } from "@ngx-translate/core";
import { ToastrModule } from "ngx-toastr";
import { ManufacturerService } from "src/app/services/manufacturer.service";
import { ProductService } from "src/app/services/product.service";
import { ManufactureListProductsComponent } from "./manufacture-list-products.component";
import { of } from 'rxjs';
import { Product } from "src/app/product/product";
import { faker } from "@faker-js/faker";

describe('ManufactureListProductsComponent', () => {
  let component: ManufactureListProductsComponent;
  let fixture: ComponentFixture<ManufactureListProductsComponent>;
  let debug: DebugElement;

  let manufacturerService: jasmine.SpyObj<ManufacturerService>;
  let productService: jasmine.SpyObj<ProductService>;

  const mockManufacturers = [
    { id: '1', name: 'Manufacturer 1', address: '123 Street', phone: '123456789', email: 'contact@test.de', country: 'USA', tax_conditions: 'Tax1', legal_conditions: 'Legal1', rating_quality: 5 },
    { id: '2', name: 'Manufacturer 2', address: '456 Avenue', phone: '987654321', email: 'support@test.no', country: 'CANADA', tax_conditions: 'Tax2', legal_conditions: 'Legal2', rating_quality: 4 },
    { id: '3', name: 'Manufacturer 3', address: '789 Boulevard', phone: '555555555', email: 'test@hotmail.com', country: 'MEXICO', tax_conditions: 'Tax3', legal_conditions: 'Legal3', rating_quality: 3 },
  ];

  const mockProducts: Product[] = [
    new Product(faker.string.uuid(), faker.string.uuid(), faker.commerce.productName(), faker.commerce.productDescription(), 'ELECTRONICS', faker.number.int({ min: 1, max: 1000 }), 'USD', false, 0, '', faker.image.url(), faker.lorem.sentence(), 2),
    new Product(faker.string.uuid(), faker.string.uuid(), faker.commerce.productName(), faker.commerce.productDescription(), 'CLOTHING', faker.number.int({ min: 1, max: 1000 }), 'EUR', true, faker.number.int({ min: 1, max: 500 }), faker.date.future().toISOString(), faker.image.url(), faker.lorem.sentence(), null),
  ];

  beforeEach(async () => {
    const manufacturerServiceMock = jasmine.createSpyObj('ManufacturerService', ['getManufacturersByList']);
    const productServiceMock = jasmine.createSpyObj('ProductService', ['getProductsByManufactureId']);

    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        ReactiveFormsModule,
        FormsModule,
        TranslateModule.forRoot(),
        ToastrModule.forRoot(),
      ],
      providers: [
        TranslateService,
        { provide: ManufacturerService, useValue: manufacturerServiceMock },
        { provide: ProductService, useValue: productServiceMock },
      ],
      declarations: [ManufactureListProductsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ManufactureListProductsComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    manufacturerService = TestBed.inject(ManufacturerService) as jasmine.SpyObj<ManufacturerService>;
    productService = TestBed.inject(ProductService) as jasmine.SpyObj<ProductService>;
  });

  beforeEach(() => {
    manufacturerService.getManufacturersByList.and.returnValue(of({
      manufacturers: mockManufacturers,
      total: mockManufacturers.length,
      page: 1,
      per_page: 10,
    }));
    productService.getProductsByManufactureId.and.returnValue(of(mockProducts));
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should list manufacturers on init', () => {
    expect(manufacturerService.getManufacturersByList).toHaveBeenCalledWith(1, 10);
    expect(component.manufacturerPaginated.manufacturers.length).toBe(mockManufacturers.length);
    const tableRows = debug.queryAll(By.css('#manufacturersTable tbody tr'));
    expect(tableRows.length).toBe(10);
    expect(tableRows[0].query(By.css('td.fw-bold')).nativeElement.textContent).toContain(mockManufacturers[0].name);
  });

  it('should list products when a manufacturer is selected', fakeAsync(() => {
    component.onSelectManufacturerCheckbox(mockManufacturers[0].id);
    tick(); 
    fixture.detectChanges();

    expect(productService.getProductsByManufactureId).toHaveBeenCalledWith(component.productPage, component.productPerPage, mockManufacturers[0].id);
    expect(component.products.length).toBe(mockProducts.length);
    const productTableRows = debug.queryAll(By.css('#productsTable tbody tr'));
    expect(productTableRows.length).toBe(10);
    expect(productTableRows[0].query(By.css('td._pname')).nativeElement.textContent).toContain(mockProducts[0].name);
  }));

  it('should change page for manufacturers list', () => {
    const newPage = 2;
    manufacturerService.getManufacturersByList.and.returnValue(of({
      manufacturers: [mockManufacturers[2]],
      total: mockManufacturers.length,
      page: newPage,
      per_page: 10,
    }));

    component.onClickManufacturerPage(newPage);
    fixture.detectChanges();

    expect(manufacturerService.getManufacturersByList).toHaveBeenCalledWith(newPage, 10);
    expect(component.manufacturerPaginated.page).toBe(newPage);
    expect(component.manufacturerPaginated.manufacturers.length).toBe(1);
    const tableRows = debug.queryAll(By.css('#manufacturersTable tbody tr'));
    expect(tableRows.length).toBe(10);
    expect(tableRows[0].query(By.css('td.fw-bold')).nativeElement.textContent).toContain(mockManufacturers[2].name);
  });
});
