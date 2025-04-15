import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { forkJoin } from 'rxjs';
import { AssociateSeller, Client, PaginatedClients } from 'src/app/dtos/client';
import { PaginatedSellers, SellerDTO } from 'src/app/dtos/seller.dto';
import { ClientService } from 'src/app/services/client.service';
import { SellerService } from 'src/app/services/seller.service';
import { UtilPagination } from 'src/app/utils/util-pagination';
@Component({
  selector: 'app-salespeople-assign-customers',
  templateUrl: './salespeople-assign-customers.component.html',
  styleUrls: ['./salespeople-assign-customers.component.css']
})
export class SalespeopleAssignCustomersComponent implements OnInit {
  constructor(
      private toastr: ToastrService,
      private readonly sellerService: SellerService,
      private readonly clientService: ClientService,
      private translate: TranslateService
    ) {}

    // Sellers
    sellers: SellerDTO[] = [];
    selectedSeller: SellerDTO | null = null;
    sellerPage = 1;
    sellerPerPage = 10;
    totalSellerPages = 0;
    sellerSortBy = 'name';
    sellerSortOrder: 'asc' | 'desc' = 'asc';
  
    // Clients
    clients: Client[] = [];
    clientPage = 1;
    clientPerPage = 10;
    totalClientPages = 0;
    clientSortBy = 'name';
    clientSortOrder: 'asc' | 'desc' = 'asc';
    selectedClients: Client[] = [];

    dataLoaded : boolean = false;
    savingData: boolean = false;

    associatedClientIds: Set<string> = new Set();
    manuallySelectedClientIds: Set<string> = new Set();
  
    ngOnInit(): void {
      forkJoin({
        sellers: this.sellerService.getSellersPaginated(
          this.sellerPage, 
        this.sellerPerPage,
        this.sellerSortBy,
        this.sellerSortOrder),
        clients: this.clientService.getAllClients(
        this.clientPage,
        this.clientPerPage,
        this.clientSortBy,
        this.clientSortOrder),
      }).subscribe(({ sellers, clients }) => {
        this.sellers = sellers.data;
        this.totalSellerPages = sellers.total_pages;
        this.clients = clients.data;
        this.totalClientPages = clients.total_pages;
        this.dataLoaded = true;
      });
    }
  
    initClients(): void{
      this.selectedClients = [];
      this.clientPage = 1;
      this.clientPerPage = 10;
      this.totalClientPages = 0;
      this.clientSortBy = 'name';
      this.clientSortOrder = 'asc';
    
    }
  
    fetchSellers(): void {
      this.sellerService.getSellersPaginated(
        this.sellerPage, 
        this.sellerPerPage,
        this.sellerSortBy,
        this.sellerSortOrder
      ).subscribe({
        next: (res: PaginatedSellers) => {
          this.sellers = res.data;
          this.totalSellerPages = res.total_pages;
        },
        error: (err) => {
          this.toastr.error(
            this.translate.instant('SALESPEOPLE.LIST_ERROR_SALESPEOPLE'),
            this.translate.instant('SALESPEOPLE.LIST_ERROR_TITLE'),
            { closeButton: true },
          );
          console.error('Error fetching sellers:', err);
        }
      });
    }
  
    onSelectSellerCheckbox(seller: SellerDTO): void {
      this.selectedSeller = null;
      this.associatedClientIds.clear();
      this.manuallySelectedClientIds.clear();
      if (this.selectedSeller === seller) {
        // Uncheck if the same seller is clicked again
        return;
      } else {
        // Select new seller
        this.onSelectSeller(seller); // this handles fetching clients
      }
    }
    onSelectSeller(seller: SellerDTO): void {
      this.selectedSeller = seller;
      this.clients.forEach(client => {
        if (client.seller_id === seller.id) {
          this.associatedClientIds.add(client.id);
        }
      });

    }

    toggleClientSelection(client: Client): void {
      const clientId = client.id;
      const isAssociated = this.associatedClientIds.has(clientId);
      const isManuallySelected = this.manuallySelectedClientIds.has(clientId);
      if (isAssociated || isManuallySelected) return;
      this.manuallySelectedClientIds.add(clientId);

    }
    isClientChecked(client: Client): boolean {
      return this.associatedClientIds.has(client.id) || this.manuallySelectedClientIds.has(client.id);
    }
  
    isClientDisabled(client: Client): boolean {
      return this.associatedClientIds.has(client.id) || this.manuallySelectedClientIds.has(client.id);
    }

    saveAssociations(): void {
      this.savingData = true;
      if (!this.selectedSeller) {
        this.savingData = false;
        return;}
  
      const newAssociations = Array.from(this.manuallySelectedClientIds);
      const associationDTO:AssociateSeller = {
        seller_id: this.selectedSeller.id,
        client_id: newAssociations
      } 
      this.clientService.saveAssociationSellerClients(associationDTO, 
        this.clientPage,
        this.clientPerPage,
        this.clientSortBy,
        this.clientSortOrder).subscribe({
          next: (res: PaginatedClients) => {
            this.clients = res.data;
            this.totalClientPages = res.total_pages;
            
            this.associatedClientIds.clear();
            this.manuallySelectedClientIds.clear();
            this.onSelectSeller(this.selectedSeller);
            this.toastr.success(
              this.translate.instant('SALESPEOPLE.ASSOCIATE_SUCCESS_MESSAGE'),
              this.translate.instant('SALESPEOPLE.ASSOCIATE_SUCCESS_TITLE'),
              { closeButton: true },
            );
            this.savingData = false;
          },
          error: (err) => {
            this.toastr.error(
              this.translate.instant('SALESPEOPLE.ASSOCIATE_ERROR_MESSAGE'),
              this.translate.instant('SALESPEOPLE.ASSOCIATE_ERROR_TITLE'),
              { closeButton: true },
            );
            console.error('Error associating clients to seller:', err);
            this.savingData = false;
          }
      });
    }


    fetchClients(): void {
  
      this.clientService.getAllClients(
        this.clientPage,
        this.clientPerPage,
        this.clientSortBy,
        this.clientSortOrder
      ).subscribe({
        next: (res: PaginatedClients) => {
          this.clients = res.data;
          this.totalClientPages = res.total_pages;
          if(this.selectedSeller){
            this.onSelectSeller(this.selectedSeller);
          }
        },
        error: (err) => {
          this.toastr.error(
            this.translate.instant('SALESPEOPLE.LIST_ERROR_CUSTOMER'),
            this.translate.instant('SALESPEOPLE.LIST_ERROR_TITLE'),
            { closeButton: true },
          );
          console.error('Error fetching clients:', err);
        }
      });
    }

  
    toggleClientSortOrder(): void {
      this.clientSortOrder = this.clientSortOrder === 'asc' ? 'desc' : 'asc';
      this.fetchClients();
    }
    toggleSellerSortOrder(): void {
      this.initClients();
      this.sellerSortOrder = this.sellerSortOrder === 'asc' ? 'desc' : 'asc';
      this.fetchSellers();
    }
  
    selectedClient: Client | null = null;
  
    /*onSelectClientCheckbox(client: Client): void {
      this.selectedClient = this.selectedClient === client ? null : client;
    }*/
  
    getPaginationSellerPages(current: number, total: number): (number | string)[] {
      return UtilPagination.getPages(current, total);
    }
    changeSellerPage(delta: number): void {
      const newPage = this.sellerPage + delta;
      if (newPage >= 1 && newPage <= this.totalSellerPages) {
        this.sellerPage = newPage;
        this.fetchSellers();
      }
    }
  
    setSellerPage(pageNumber: number): void {
      if (pageNumber !== this.sellerPage) {
        this.sellerPage = pageNumber;
        this.fetchSellers();
      }
    }
    onClickSellerPage(page: number | string): void {
      if (typeof page === 'number' && page !== this.sellerPage) {
        this.setSellerPage(page);
      }
    }
  
    getPaginationClientPages(current: number, total: number): (number | string)[] {
      return UtilPagination.getPages(current, total);;
    }
    changeClientPage(delta: number): void {
      const newPage = this.clientPage + delta;
      if (newPage >= 1 && newPage <= this.totalClientPages) {
        this.clientPage = newPage;
        this.fetchClients();
      }
    }
  
    setClientPage(pageNumber: number): void {
      if (pageNumber !== this.clientPage) {
        this.clientPage = pageNumber;
        this.fetchClients();
      }
    }
    onClickClientPage(page: number | string): void {
      if (typeof page === 'number' && page !== this.clientPage) {
        this.setClientPage(page);
        
      }
      console.log(this.associatedClientIds)
    }
}
