import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { StoreAssignProductComponent } from './store-assign-product.component';
import { StoreService } from 'src/app/services/store.service';
import { ProductService } from 'src/app/services/product.service';
import { StocksService } from 'src/app/services/stocks.service';
import { ToastrService } from 'ngx-toastr';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { of } from 'rxjs';
import { FormsModule } from '@angular/forms';

// Dummy responses based on DTO structures.
const dummyStoresResponse = {
  data: [
    { 
      id: 'store1', 
      name: 'Carrefour', 
      phone: '111', 
      email: 'a@a.com', 
      address: 'Address 1', 
      capacity: 100, 
      state: 'ACTIVE', 
      security_level: 'MEDIUM', 
      created_at: new Date(), 
      updated_at: new Date() 
    },
    { 
      id: 'store2', 
      name: 'Cencosud', 
      phone: '222', 
      email: 'b@b.com', 
      address: 'Address 2', 
      capacity: 200, 
      state: 'ACTIVE', 
      security_level: 'MEDIUM', 
      created_at: new Date(), 
      updated_at: new Date() 
    }
  ],
  page: 1,
  per_page: 10,
  total: 2,
  total_pages: 1
};

const dummyProductsResponse = {
  data: [
    { 
      id: 'prod1', 
      name: 'Chocolate Bar', 
      category: 'Food', 
      currency_price: 'USD', 
      description: 'Delicious chocolate', 
      discount_price: 0, 
      expired_at: new Date('2025-01-01T00:00:00Z'), 
      is_promotion: false, 
      manufacturer_id: 'm1', 
      store_conditions: '', 
      unit_price: 1, 
      created_at: new Date(), 
      updated_at: new Date(), 
      url_photo: 'http://example.com/photo1.png'
    },
    { 
      id: 'prod2', 
      name: 'Modern Sofa', 
      category: 'Furniture', 
      currency_price: 'USD', 
      description: 'Comfortable sofa', 
      discount_price: 0, 
      expired_at: new Date('2025-01-01T00:00:00Z'), 
      is_promotion: false, 
      manufacturer_id: 'm2', 
      store_conditions: '', 
      unit_price: 500, 
      created_at: new Date(), 
      updated_at: new Date(), 
      url_photo: 'http://example.com/photo2.png'
    }
  ],
  page: 1,
  per_page: 10,
  total: 2,
  total_pages: 1
};

const dummyAssignedStocksResponse = {
  store_id: 'store1',
  stocks: [
    { id: 'stock1', product_id: 'prod1', assigned_stock: 10 }
  ]
};

describe('StoreAssignProductComponent', () => {
  let component: StoreAssignProductComponent;
  let fixture: ComponentFixture<StoreAssignProductComponent>;
  
  let storeServiceSpy: jasmine.SpyObj<StoreService>;
  let productServiceSpy: jasmine.SpyObj<ProductService>;
  let stocksServiceSpy: jasmine.SpyObj<StocksService>;
  let toastrSpy: jasmine.SpyObj<ToastrService>;
  let translateSpy: jasmine.SpyObj<TranslateService>;
  
  beforeEach(async () => {
    const storeSpy = jasmine.createSpyObj('StoreService', ['getPaginatedStores']);
    const productSpy = jasmine.createSpyObj('ProductService', ['getProductsPaginated']);
    const stocksSpy = jasmine.createSpyObj('StocksService', ['getStocksByStore', 'assignStockToStore']);
    const toastrServiceSpy = jasmine.createSpyObj('ToastrService', ['success', 'error', 'warning', 'info']);
    const translateServiceSpy = jasmine.createSpyObj('TranslateService', ['instant']);

    // Stub translations to return the key itself.
    translateServiceSpy.instant.and.callFake((key: string) => key);

    await TestBed.configureTestingModule({
      declarations: [ StoreAssignProductComponent ],
      imports: [ FormsModule, TranslateModule.forRoot() ],
      providers: [
        { provide: StoreService, useValue: storeSpy },
        { provide: ProductService, useValue: productSpy },
        { provide: StocksService, useValue: stocksSpy },
        { provide: ToastrService, useValue: toastrServiceSpy },
        { provide: TranslateService, useValue: translateServiceSpy }
      ]
    }).compileComponents();
    
    storeServiceSpy = TestBed.inject(StoreService) as jasmine.SpyObj<StoreService>;
    productServiceSpy = TestBed.inject(ProductService) as jasmine.SpyObj<ProductService>;
    stocksServiceSpy = TestBed.inject(StocksService) as jasmine.SpyObj<StocksService>;
    toastrSpy = TestBed.inject(ToastrService) as jasmine.SpyObj<ToastrService>;
    translateSpy = TestBed.inject(TranslateService) as jasmine.SpyObj<TranslateService>;
    
    // Set default return values for service methods, so that both loadStores and loadProducts work.
    storeServiceSpy.getPaginatedStores.and.returnValue(of(dummyStoresResponse));
    productServiceSpy.getProductsPaginated.and.returnValue(of(dummyProductsResponse));
    
    fixture = TestBed.createComponent(StoreAssignProductComponent);
    component = fixture.componentInstance;
  });
  
  it('should create the component', () => {
    expect(component).toBeTruthy();
  });
  
  it('should load stores on init and transform store image', fakeAsync(() => {
    storeServiceSpy.getPaginatedStores.and.returnValue(of(dummyStoresResponse));
    component.ngOnInit();
    tick();
    expect(component.stores.length).toBe(2);
    expect(component.stores[0].name).toBe('Carrefour');
    expect(component.stores[0].image).toBe('carrefour.png');
  }));
  
  it('should load products on init and compute local_image', fakeAsync(() => {
    productServiceSpy.getProductsPaginated.and.returnValue(of(dummyProductsResponse));
    component.ngOnInit();
    tick();
    expect(component.products.length).toBe(2);
    expect(component.products[0].name).toBe('Chocolate Bar');
    expect(component.products[0].local_image).toBe('chocolate_bar.png');
  }));
  
  it('should toggle product selection and update hasChanges', () => {
    const product = {
      id: 'prod1',
      name: 'Chocolate Bar',
      category: 'Food',
      currency_price: 'USD',
      description: 'Delicious chocolate',
      discount_price: 0,
      expired_at: new Date('2025-01-01T00:00:00Z'),
      is_promotion: false,
      manufacturer_id: 'm1',
      store_conditions: '',
      unit_price: 1,
      created_at: new Date(),
      updated_at: new Date(),
      url_photo: 'http://example.com/photo1.png',
      selected: false,
      quantity: 0,
      local_image: 'chocolate_bar.png'
    };
    component.products = [ product ];
    component.onProductSelect(product);
    expect(product.selected).toBeTrue();
    expect(component.productSelections[product.id].selected).toBeTrue();
    expect(component.hasChanges).toBeTrue();
    
    // Toggle again to unselect.
    component.onProductSelect(product);
    expect(product.selected).toBeFalse();
    expect(product.quantity).toBe(0);
  });
  
  it('should update product quantity and mark hasChanges', () => {
    const product = {
      id: 'prod1',
      name: 'Chocolate Bar',
      category: 'Food',
      currency_price: 'USD',
      description: 'Delicious chocolate',
      discount_price: 0,
      expired_at: new Date('2025-01-01T00:00:00Z'),
      is_promotion: false,
      manufacturer_id: 'm1',
      store_conditions: '',
      unit_price: 1,
      created_at: new Date(),
      updated_at: new Date(),
      url_photo: 'http://example.com/photo1.png',
      selected: true,
      quantity: 0,
      local_image: 'chocolate_bar.png'
    };
    component.products = [ product ];
    product.quantity = 5;
    component.onProductQuantityChange(product);
    expect(product.quantity).toBe(5);
    expect(component.productSelections[product.id].quantity).toBe(5);
    expect(component.hasChanges).toBeTrue();
  });
  
  it('should load assigned stocks when a store is selected', fakeAsync(() => {
    component.products = [
      {
        id: 'prod1',
        name: 'Chocolate Bar',
        category: 'Food',
        currency_price: 'USD',
        description: 'Delicious chocolate',
        discount_price: 0,
        expired_at: new Date('2025-01-01T00:00:00Z'),
        is_promotion: false,
        manufacturer_id: 'm1',
        store_conditions: '',
        unit_price: 1,
        created_at: new Date(),
        updated_at: new Date(),
        url_photo: 'http://example.com/photo1.png',
        selected: false,
        quantity: 0,
        local_image: 'chocolate_bar.png'
      },
      {
        id: 'prod2',
        name: 'Modern Sofa',
        category: 'Furniture',
        currency_price: 'USD',
        description: 'Comfortable sofa',
        discount_price: 0,
        expired_at: new Date('2025-01-01T00:00:00Z'),
        is_promotion: false,
        manufacturer_id: 'm2',
        store_conditions: '',
        unit_price: 500,
        created_at: new Date(),
        updated_at: new Date(),
        url_photo: 'http://example.com/photo2.png',
        selected: false,
        quantity: 0,
        local_image: 'modern_sofa.png'
      }
    ];
    stocksServiceSpy.getStocksByStore.and.returnValue(of(dummyAssignedStocksResponse));
    component.onSelectStore({ id: 'store1', name: 'Carrefour', phone: '111', email: 'a@a.com', address: 'Address 1', capacity: 100, state: 'ACTIVE', security_level: 'MEDIUM', image: 'carrefour.png' });
    tick();
    const prod1 = component.products.find(p => p.id === 'prod1');
    const prod2 = component.products.find(p => p.id === 'prod2');
    expect(prod1?.selected).toBeTrue();
    expect(prod1?.quantity).toBe(10);
    expect(prod2?.selected).toBeFalse();
    expect(prod2?.quantity).toBe(0);
  }));
  
  it('should warn if saveAssignments is called without a selected store', () => {
    component.selectedStore = null;
    component.hasChanges = true;
    component.saveAssignments();
    expect(toastrSpy.warning).toHaveBeenCalledWith('STORE.PLEASE_SELECT_STORE');
  });
  
  it('should show info if saveAssignments is called when no changes exist', () => {
    component.selectedStore = { id: 'store1', name: 'Carrefour', phone: '111', email: 'a@a.com', address: 'Address 1', capacity: 100, state: 'ACTIVE', security_level: 'MEDIUM', image: 'carrefour.png' };
    component.hasChanges = false;
    component.saveAssignments();
    expect(toastrSpy.info).toHaveBeenCalledWith('STORE.NO_CHANGES');
  });
  
  it('should call assignStockToStore on saveAssignments and reset selections', fakeAsync(() => {
    component.selectedStore = { id: 'store1', name: 'Carrefour', phone: '111', email: 'a@a.com', address: 'Address 1', capacity: 100, state: 'ACTIVE', security_level: 'MEDIUM', image: 'carrefour.png' };
    component.products = [
      {
        id: 'prod1',
        name: 'Chocolate Bar',
        category: 'Food',
        currency_price: 'USD',
        description: 'Delicious chocolate',
        discount_price: 0,
        expired_at: new Date('2025-01-01T00:00:00Z'),
        is_promotion: false,
        manufacturer_id: 'm1',
        store_conditions: '',
        unit_price: 1,
        created_at: new Date(),
        updated_at: new Date(),
        url_photo: 'http://example.com/photo1.png',
        selected: true,
        quantity: 5,
        local_image: 'chocolate_bar.png'
      },
      {
        id: 'prod2',
        name: 'Modern Sofa',
        category: 'Furniture',
        currency_price: 'USD',
        description: 'Comfortable sofa',
        discount_price: 0,
        expired_at: new Date('2025-01-01T00:00:00Z'),
        is_promotion: false,
        manufacturer_id: 'm2',
        store_conditions: '',
        unit_price: 500,
        created_at: new Date(),
        updated_at: new Date(),
        url_photo: 'http://example.com/photo2.png',
        selected: false,
        quantity: 0,
        local_image: 'modern_sofa.png'
      }
    ];
    component.hasChanges = true;
    stocksServiceSpy.assignStockToStore.and.returnValue(of({}));
    
    component.saveAssignments();
    tick();
    
    expect(stocksServiceSpy.assignStockToStore).toHaveBeenCalled();
    expect(component.hasChanges).toBeFalse();
    expect(component.selectedStore).toBeNull();
    expect(component.products.every(p => !p.selected && p.quantity === 0)).toBeTrue();
    expect(toastrSpy.success).toHaveBeenCalledWith('STORE.ASSIGN_SUCCESS');
  }));
});