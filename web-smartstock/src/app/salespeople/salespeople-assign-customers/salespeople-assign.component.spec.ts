/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { faker } from '@faker-js/faker';

import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { ClientService } from 'src/app/services/client.service';
import { SellerService } from 'src/app/services/seller.service';
import { Client, PaginatedClients } from 'src/app/dtos/client';
import { PaginatedSellers, SellerDTO } from 'src/app/dtos/seller.dto';
import { SalespeopleAssignCustomersComponent } from './salespeople-assign-customers.component';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

describe('SalesPeopleListComponent', () => {
  let component: SalespeopleAssignCustomersComponent;
  let fixture: ComponentFixture<SalespeopleAssignCustomersComponent>;
  let mockClientService: jasmine.SpyObj<ClientService>;
  let mockSellerService: jasmine.SpyObj<SellerService>;
  let mockToastrService: jasmine.SpyObj<ToastrService>;

  const mockSellers: PaginatedSellers = {
    data: [
      { id: '1', name: 'Seller 1', email: 's1@sta.com', phone: '', password: '', type: '', zone: 'CENTER', quota_expected: 1000000, currency_quota: 'COP', quartely_target: 2000000, currency_target: 'COP', performance_recomendations: 'Good', user_id: 'uid1', created_at: '', updated_at: '' }
    ],
    page: 1,
    per_page: 10,
    total: 1,
    total_pages: 1
  };

  const mockClients: PaginatedClients = {
    data: [
      { id: 'c1', name: 'Client 1', email: 'c1@sta.com', phone: '', user_id: '', zone: 'CENTER', address: '', client_type: '', created_at: '', updated_at: '', seller_id: '1' },
      { id: 'c2', name: 'Client 2', email: 'c2@sta.com', phone: '', user_id: '', zone: 'CENTER', address: '', client_type: '', created_at: '', updated_at: '' },
      { id: 'c3', name: 'Client 3', email: 'c3@sta.com', phone: '', user_id: '', zone: 'CENTER', address: '', client_type: '', created_at: '', updated_at: '' }
    ],
    page: 1,
    per_page: 10,
    total: 2,
    total_pages: 1
  };

  beforeEach(async(() => {
    mockClientService = jasmine.createSpyObj('ClientService', ['getAllClients', 'saveAssociationSellerClients']);
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
        { provide: ToastrService, useValue: mockToastrService },
        TranslateService
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      declarations: [ SalespeopleAssignCustomersComponent ]
    });

    fixture = TestBed.createComponent(SalespeopleAssignCustomersComponent);
    component = fixture.componentInstance;

    mockClientService = TestBed.inject(ClientService) as jasmine.SpyObj<ClientService>;
    mockSellerService = TestBed.inject(SellerService) as jasmine.SpyObj<SellerService>;


    mockSellerService.getSellersPaginated.and.returnValue(of(mockSellers));
    mockClientService.getAllClients.and.returnValue(of(mockClients));
    mockClientService.saveAssociationSellerClients.and.returnValue(of(mockClients));

    fixture.detectChanges();

  }));

  
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch sellers on init', () => {
    expect(component.sellers.length).toBe(1);
    expect(component.sellers[0].name).toBe('Seller 1');
  });

  it('should fetch clients on init', () => {
    expect(component.clients.length).toBe(3);
  });

  it('should allow selecting a seller', () => {
    component.onSelectSellerCheckbox(mockSellers.data[0]);
    expect(component.selectedSeller).toEqual(mockSellers.data[0]);
  });

  it('should toggle client selection correctly', () => {
    const client = mockClients.data[2]; // unassigned
    component.toggleClientSelection(client);

    expect(component.manuallySelectedClientIds.has(client.id)).toBeTrue();

  });

  it('should disable checkbox for clients already associated to seller', () => {
    const associatedClient = mockClients.data[0]; // has seller_id = '1'
    component.selectedSeller = mockSellers.data[0]; // seller_id = '1'
    component.associatedClientIds.add(associatedClient.id)
    expect(component.isClientDisabled(associatedClient)).toBeTrue();
  });

  it('should not disable checkbox for unassociated clients', () => {
    const newClient = mockClients.data[1]; // no seller_id
    component.selectedSeller = mockSellers.data[0];
    expect(component.isClientDisabled(newClient)).toBeFalse();
  });

  it('should send correct data to saveAssociationSellerClients', () => {
    const clientToAdd = mockClients.data[1];
    component.selectedSeller = mockSellers.data[0];
    component.toggleClientSelection(clientToAdd);

    component.saveAssociations();

    expect(mockClientService.saveAssociationSellerClients).toHaveBeenCalledWith(
      {
        seller_id: '1',
        client_id: [clientToAdd.id]
      },
      1,
      10,
      'name',
      'asc'
    );
  });

  it('should change seller page', () => {
    component.sellerPage = 1;
    component.totalSellerPages = 2;
    component.changeSellerPage(1); // go to page 2

    expect(mockSellerService.getSellersPaginated).toHaveBeenCalledWith(2, 10, 'name', 'asc');
  });

  it('should change client page', () => {
    component.clientPage = 1;
    component.totalClientPages = 2;
    component.changeClientPage(1); // go to page 2

    expect(mockClientService.getAllClients).toHaveBeenCalledWith(2, 10, 'name', 'asc');
  });

  it('should sort sellers by name', () => {
    const initialSort = component.sellerSortOrder;
    component.toggleSellerSortOrder();
    expect(component.sellerSortOrder).not.toBe(initialSort);
  });

  it('should sort clients by name', () => {
    const initialSort = component.clientSortOrder;
    component.toggleClientSortOrder();
    expect(component.clientSortOrder).not.toBe(initialSort);
  });

});