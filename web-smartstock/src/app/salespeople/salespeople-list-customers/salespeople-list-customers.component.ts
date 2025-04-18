import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { Client, PaginatedClients } from 'src/app/dtos/client';
import { PaginatedSellers, SellerDTO } from 'src/app/dtos/seller.dto';
import { ClientService } from 'src/app/services/client.service';
import { SellerService } from 'src/app/services/seller.service';
import { UtilPagination } from 'src/app/utils/util-pagination';

@Component({
  selector: 'app-salespeople-list-customers',
  templateUrl: './salespeople-list-customers.component.html',
  styleUrls: ['./salespeople-list-customers.component.css']
})
export class SalespeopleListCustomersComponent implements OnInit {
  constructor(
    private toastr: ToastrService,
    private readonly sellerService: SellerService,
    private readonly clientService: ClientService,
    private translate: TranslateService
  ) {}
  initialEntry: boolean = true;
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

  ngOnInit(): void {
    this.fetchSellers();
  }

  initClients(): void{
    this.clients = [];
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

    if (this.selectedSeller === seller) {
      // Uncheck if the same seller is clicked again
      this.selectedSeller = null;
      this.clients = [];
      this.totalClientPages = 0;
    } else {
      // Select new seller
      this.onSelectSeller(seller); // this handles fetching clients
    }
  }
  onSelectSeller(seller: SellerDTO): void {
    this.initClients();
    this.initialEntry = false;
    this.selectedSeller = seller;
    this.clientPage = 1; // Reset client page when new seller is selected
    this.fetchClients();
  }

  fetchClients(): void {
    if (!this.selectedSeller) return;

    this.clientService.getClientsBySellerId(
      this.selectedSeller.id,
      this.clientPage,
      this.clientPerPage,
      this.clientSortBy,
      this.clientSortOrder
    ).subscribe({
      next: (res: PaginatedClients) => {
        this.clients = res.data;
        this.totalClientPages = res.total_pages;
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
  /*changeSellerPage(delta: number): void {
    this.sellerPage += delta;
    this.fetchSellers();
  }*/

  /*changeClientPage(delta: number): void {
    if (!this.selectedSeller) return;

    this.clientPage += delta;
    this.fetchClients();
  }*/

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

  onSelectClientCheckbox(client: Client): void {
    this.selectedClient = this.selectedClient === client ? null : client;
  }

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
  }
}
