/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { faker } from '@faker-js/faker';

import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { TranslateModule } from '@ngx-translate/core';
import { ClientService } from 'src/app/services/client.service';
import { SellerService } from 'src/app/services/seller.service';
import { SalespeopleListCustomersComponent } from './salespeople-list-customers.component';
import { Client, PaginatedClients } from 'src/app/dtos/client';
import { PaginatedSellers, SellerDTO } from 'src/app/dtos/seller.dto';

describe('SalesPeopleListComponent', () => {
  let component: SalespeopleListCustomersComponent;
  let fixture: ComponentFixture<SalespeopleListCustomersComponent>;
  let mockClientService: jasmine.SpyObj<ClientService>;
  let mockSellerService: jasmine.SpyObj<SellerService>;
  let mockToastrService: jasmine.SpyObj<ToastrService>;

  beforeEach(async(() => {
    mockClientService = jasmine.createSpyObj('ClientService', ['getClientsBySellerId']);
    mockSellerService = jasmine.createSpyObj('SellerService', ['getSellersPaginated']);
    mockToastrService = jasmine.createSpyObj('ToastrService', ['success', 'error']);


    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        TranslateModule.forRoot()
      ],
      providers: [
        { provide: ClientService, useValue: mockClientService },
        { provide: SellerService, useValue: mockSellerService },
        { provide: ToastrService, useValue: mockToastrService }
      ],
      declarations: [ SalespeopleListCustomersComponent ]
    });

    fixture = TestBed.createComponent(SalespeopleListCustomersComponent);
    component = fixture.componentInstance;

  }));

  
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch sellers on init', () => {
    const fakeSellers: PaginatedSellers = {
      data: [{ 
        id: faker.string.uuid(),
        name: 'Seller A',
        phone:'11111111111',
        email:'email@email.com',
        password:'21333333',
        type:'SELLER',
        zone:'CENTER',
        quota_expected: 1000.0,
        currency_target: 'COP',
        currency_quota: 'COP',
        quartely_target: 1000,
        performance_recomendations: 'N'
       }],
       total_pages: 1,
       page: 1,
       per_page: 10,
       total: 1
    };
    mockSellerService.getSellersPaginated.and.returnValue(of(fakeSellers));

    component.ngOnInit();

    expect(mockSellerService.getSellersPaginated).toHaveBeenCalled();
    expect(component.sellers.length).toBe(1);
    expect(component.totalSellerPages).toBe(1);
  });

  it('should handle seller fetch error', () => {
    spyOn(console, 'error');
    mockSellerService.getSellersPaginated.and.returnValue(throwError(() => new Error('Fetch failed')));

    component.fetchSellers();

    expect(console.error).toHaveBeenCalledWith('Error fetching sellers:', jasmine.any(Error));
  });

  it('should select and unselect seller', () => {
    const seller: SellerDTO = { 
      id: faker.string.uuid(),
      name: 'Seller B',
      phone:'11111111111',
      email:'email@email.com',
      password:'21333333',
      type:'SELLER',
      zone:'CENTER',
      quota_expected: 1000.0,
      currency_target: 'COP',
      currency_quota: 'COP',
      quartely_target: 1000,
      performance_recomendations: 'N'
     };
    spyOn(component, 'onSelectSeller');

    component.selectedSeller = seller;
    component.onSelectSellerCheckbox(seller);

    expect(component.selectedSeller).toBeNull();

    component.selectedSeller = null;
    component.onSelectSellerCheckbox(seller);

    expect(component.onSelectSeller).toHaveBeenCalledWith(seller);
  });

  it('should fetch clients when seller selected', () => {
    const seller: SellerDTO = { 
      id: faker.string.uuid(),
      name: 'Seller C',
      phone:'11111111111',
      email:'email@email.com',
      password:'21333333',
      type:'SELLER',
      zone:'CENTER',
      quota_expected: 1000.0,
      currency_target: 'COP',
      currency_quota: 'COP',
      quartely_target: 1000,
      performance_recomendations: 'N'
     };
    const fakeClients: PaginatedClients = {
      data: [{ 
          id: faker.string.uuid(),
          user_id: faker.string.uuid(),
          created_at:'Thu, 10 Apr 2025 08:54:51 GMT',
          updated_at:'Thu, 10 Apr 2025 08:54:51 GMT',
          name: 'Client A',
          address: 'AAAAAAA',
          phone:'11111111111',
          client_type: 'CORNER_STORE',
          email:'email@email.com',
          zone:'CENTER'
        }],
      total_pages: 1,
      page: 1,
      per_page: 10,
      total: 1
    };
    component.selectedSeller = seller;
    mockClientService.getClientsBySellerId.and.returnValue(of(fakeClients));

    component.fetchClients();

    expect(component.clients.length).toBe(1);
    expect(component.totalClientPages).toBe(1);
  });

  it('should not fetch clients if no seller is selected', () => {
    component.selectedSeller = null;
    component.fetchClients();

    expect(mockClientService.getClientsBySellerId).not.toHaveBeenCalled();
  });

  it('should toggle sort order for sellers and refetch', () => {
    component.sellerSortOrder = 'asc';
    spyOn(component, 'fetchSellers');
    spyOn(component, 'initClients');

    component.toggleSellerSortOrder();

    expect(component.sellerSortOrder).toBe('desc');
    expect(component.initClients).toHaveBeenCalled();
    expect(component.fetchSellers).toHaveBeenCalled();
  });

  it('should change client page within bounds', () => {
    const seller: SellerDTO = { 
      id: faker.string.uuid(),
      name: 'Seller C',
      phone:'11111111111',
      email:'email@email.com',
      password:'21333333',
      type:'SELLER',
      zone:'CENTER',
      quota_expected: 1000.0,
      currency_target: 'COP',
      currency_quota: 'COP',
      quartely_target: 1000,
      performance_recomendations: 'N'
     };
    component.selectedSeller = seller;
    component.clientPage = 1;
    component.totalClientPages = 3;
    spyOn(component, 'fetchClients');

    component.changeClientPage(1);

    expect(component.clientPage).toBe(2);
    expect(component.fetchClients).toHaveBeenCalled();
  });

  it('should not change page out of bounds', () => {
    component.clientPage = 1;
    component.totalClientPages = 2;
    spyOn(component, 'fetchClients');

    component.changeClientPage(-1);
    expect(component.clientPage).toBe(1);
    expect(component.fetchClients).not.toHaveBeenCalled();
  });

  it('should set client page only if different', () => {
    component.clientPage = 1;
    spyOn(component, 'fetchClients');

    component.setClientPage(2);
    expect(component.clientPage).toBe(2);
    expect(component.fetchClients).toHaveBeenCalled();
  });

  it('should toggle client checkbox selection', () => {
    const client: Client = { 
      id: faker.string.uuid(),
      user_id: faker.string.uuid(),
      created_at:'Thu, 10 Apr 2025 08:54:51 GMT',
      updated_at:'Thu, 10 Apr 2025 08:54:51 GMT',
      name: 'Client A',
      address: 'AAAAAAA',
      phone:'11111111111',
      client_type: 'CORNER_STORE',
      email:'email@email.com',
      zone:'CENTER'
    };
    component.selectedClient = null;

    component.onSelectClientCheckbox(client);
    expect(component.selectedClient).toBe(client);

    component.onSelectClientCheckbox(client);
    expect(component.selectedClient).toBeNull();
  });

  it('should generate correct pagination range', () => {
    const result = component.getPaginationSellerPages(5, 10);
    expect(result).toContain(1);
    expect(result).toContain('...');
    expect(result).toContain(5);
    expect(result).toContain(10);
  });

});