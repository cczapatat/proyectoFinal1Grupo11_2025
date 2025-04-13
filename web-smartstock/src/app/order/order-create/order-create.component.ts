import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { ClientDTO } from 'src/app/dtos/client.dto';
import { ProductStockDTO } from 'src/app/dtos/stock.dto';
import { SellerDTO } from 'src/app/dtos/seller.dto';
import { OrderCreateDTO } from "src/app/dtos/order.dto";

import { ClientService } from 'src/app/services/client.service';
import { StocksService } from 'src/app/services/stocks.service';
import { SellerService } from 'src/app/services/seller.service';
import { OrderService } from 'src/app/services/order.service';

import { UtilAToken } from 'src/app/utils/util-token';
import { UtilPagination } from 'src/app/utils/util-pagination';

interface Product extends ProductStockDTO {
  quantitySelected?: number;
}

interface InfoProductStocksPaginate {
  page: number;
  per_page: number;
  total: number;
  total_page: number;
}

const PAGE = 1;
const PER_PAGE = 5;

@Component({
  selector: 'app-order-create',
  templateUrl: './order-create.component.html',
  styleUrls: ['./order-create.component.css']
})
export class OrderCreateComponent implements OnInit {
  sellers: SellerDTO[] = [];
  selectedSeller: string = '';

  clients: ClientDTO[] = [];
  selectedClient: string = '';

  deliveryDate: string = '';

  selectedPayment: string = '';
  paymentMethods = [];

  products: Product[] = [];
  availableProducts: Product[] = [];

  selectedModalProducts: { [id: string]: number } = {};
  infoProductStocksPaginate: InfoProductStocksPaginate = { page: PAGE, per_page: PER_PAGE, total: 0, total_page: 0 };

  isAdmin: boolean = false;

  constructor(
    private toastr: ToastrService,
    private translate: TranslateService,
    private clientService: ClientService,
    private sellerService: SellerService,
    private stocksService: StocksService,
    private orderService: OrderService,
  ) {
    this.isAdmin = UtilAToken.isAdmin();
  }

  ngOnInit(): void {
    if (this.isAdmin) {
      this.loadDataAsAdmin();
    } else {
      this.selectedSeller = UtilAToken.getUserId();
      this.loadDataAsSeller(this.selectedSeller);
    }
    this.loadResources();
    this.deliveryDate = this.formatDate(new Date());
  }

  loadDataAsAdmin() {
    this.sellerService.getSellersList().subscribe({
      next: (response) => {
        this.sellers = response;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('ORDER.CREATE_LOAD_DATA_SELLERS_ERROR_MESSAGE'),
          this.translate.instant('ORDER.CREATE_LOAD_DATA_SELLERS_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    })
  }

  loadDataAsSeller(sellerId: string): void {
    this.clientService.getClientsBySellerIdList(sellerId).subscribe({
      next: (response) => {
        this.clients = response;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('ORDER.CREATE_LOAD_DATA_CLIENTS_ERROR_MESSAGE'),
          this.translate.instant('ORDER.CREATE_LOAD_DATA_CLIENTS_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });
  }

  loadResources() {
    this.loadProductStocks();
    this.loadPaymentMethods();
  }

  loadProductStocks() {
    this.stocksService.getProductsOnStock(this.infoProductStocksPaginate.page, this.infoProductStocksPaginate.per_page)
      .subscribe({
        next: (response) => {
          this.infoProductStocksPaginate = {
            page: response.page,
            per_page: response.per_page,
            total: response.total,
            total_page: Math.ceil(response.total / response.per_page),
          };
          this.availableProducts = response.stocks.map((p: ProductStockDTO) => ({
            ...p,
            quantitySelected: 1,
            selected: !!this.selectedModalProducts[p.id],
          }));
        },
        error: (error) => {
          this.toastr.error(
            this.translate.instant('ORDER.CREATE_LOAD_DATA_STOCKS_ERROR_MESSAGE'),
            this.translate.instant('ORDER.CREATE_LOAD_DATA_STOCKS_ERROR_TITLE'),
            { closeButton: true },
          );
        }
      });
  }

  loadPaymentMethods() {
    this.orderService.getPaymentMethods().subscribe({
      next: (response) => {
        this.paymentMethods = response;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('ORDER.CREATE_LOAD_DATA_PAYMENTS_ERROR_MESSAGE'),
          this.translate.instant('ORDER.CREATE_LOAD_DATA_PAYMENTS_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    })
  }

  formatDate(date: Date): string {
    return date.toISOString().slice(0, 10);
  }

  selectSellerFromAdmin() {
    this.selectedClient = '';
    this.clients = [];

    if (this.selectedSeller != '') {
      this.loadDataAsSeller(this.selectedSeller);
    }
  }

  incrementQuantity(product: Product) {
    product.quantitySelected++;
  }

  decrementQuantity(product: Product) {
    if (product.quantitySelected > 1) {
      product.quantitySelected--;
    }
  }

  removeProduct(product: Product) {
    const index = this.products.findIndex(p => p.id === product.id)
    this.products.splice(index, 1);
  }

  get getTotal(): number {
    return this.products.reduce((total, prod) => total + (prod.product.unit_price * prod.quantitySelected), 0);
  }

  hasSelectedProductStock(productId: string): Boolean {
    return !!this.selectedModalProducts[productId]
  }

  toggleSelectProduct(product: Product) {
    const selected = this.hasSelectedProductStock(product.id);
    if (!selected) {
      this.selectedModalProducts[product.id] = product.quantity_in_stock;
    } else {
      delete this.selectedModalProducts[product.id];
      this.removeProduct(product);
    }
  }

  increaseModalQuantity(productId: string, quantity: number) {
    if (this.selectedModalProducts[productId] < quantity) {
      this.selectedModalProducts[productId]++;
    }
  }

  decreaseModalQuantity(productId: string) {
    if (this.selectedModalProducts[productId] > 1) {
      this.selectedModalProducts[productId]--;
    }
  }

  addProductsToOrder() {
    Object.entries(this.selectedModalProducts).forEach(([id, quantity]) => {
      const product = this.availableProducts.find(p => p.id === id);
      if (product) {
        const existing = this.products.find(p => p.id === id);
        if (existing) {
          existing.quantitySelected = quantity;
        } else {
          this.products.push({ ...product, quantitySelected: quantity });
        }
      }
    });
  }

  getPaginationProductStocksPages(current: number, total: number): (number | string)[] {
    return UtilPagination.getPages(current, total);
  }

  setPage(page: number) {
    const pageCurr = this.infoProductStocksPaginate.page + page;

    if (pageCurr <= 0) {
      this.infoProductStocksPaginate.page = 1;
    } else if (pageCurr > this.infoProductStocksPaginate.total_page) {
      this.infoProductStocksPaginate.page = this.infoProductStocksPaginate.total_page;
    } else {
      this.infoProductStocksPaginate.page = pageCurr;
    }
    this.loadProductStocks();
  }

  setPagePos(page: number) {
    this.infoProductStocksPaginate.page = page;
    this.loadProductStocks();
  }

  get validOrder(): boolean {
    return this.selectedSeller !== '' && this.selectedClient !== '' && this.products.length > 0 && this.deliveryDate !== '' && this.selectedPayment !== '';
  }

  resetForm() {
    this.selectedSeller = '';
    this.selectedClient = '';
    this.deliveryDate = this.formatDate(new Date());
    this.selectedPayment = '';
    this.products = [];
    this.selectedModalProducts = {};
    this.availableProducts = [];
    this.infoProductStocksPaginate = { page: PAGE, per_page: PER_PAGE, total: 0, total_page: 0 };
    this.loadProductStocks();
  }

  createOrder() {
    const newOrder: OrderCreateDTO = {
      client_id: this.selectedClient,
      delivery_date: `${this.deliveryDate} 00:00:00`,
      payment_method: this.selectedPayment,
      products: this.products.map(p => ({
        product_id: p.id,
        units: p.quantitySelected,
      })),
    };

    if (this.isAdmin) {
      newOrder.seller_id = this.selectedSeller;
    }

    this.orderService.createOrder(newOrder).subscribe({
      next: (response) => {
        this.toastr.success(
          this.translate.instant('ORDER.CREATE_SUCCESS_MESSAGE'),
          this.translate.instant('ORDER.CREATE_SUCCESS_TITLE'),
          { closeButton: true },
        );
        this.resetForm();
      },
      error: (error) => {
        console.error(error);
        this.toastr.error(
          this.translate.instant('ORDER.CREATE_ERROR_MESSAGE'),
          this.translate.instant('ORDER.CREATE_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });
  }
}
