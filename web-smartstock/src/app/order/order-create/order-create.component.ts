import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { forkJoin } from 'rxjs';
import { ClientDTO } from 'src/app/dtos/client.dto';

import { ClientService } from 'src/app/services/client.service';

interface Product {
  id: number;
  name: string;
  description: string;
  unitPrice: number;
  quantity: number;
  quantitySelected?: number;
  selected: boolean;
}

@Component({
  selector: 'app-order-create',
  templateUrl: './order-create.component.html',
  styleUrls: ['./order-create.component.css']
})
export class OrderCreateComponent implements OnInit {
  clients: ClientDTO[] = [];
  selectedClient: string = '';

  deliveryDate: string = '';

  selectedPayment: string = 'Cash On Delivery';
  paymentMethods = ['Cash On Delivery', 'Debit Card', 'Credit Card'];

  products: Product[] = [];
  availableProducts: Product[] = [];

  selectedModalProducts: { [id: number]: number } = {};

  currentPage: number = 1;
  pageSize: number = 5;

  constructor(
    private toastr: ToastrService,
    private translate: TranslateService,
    private clientService: ClientService,
  ) { }

  ngOnInit(): void {
    this.loadData();
    this.deliveryDate = this.formatDate(new Date());

    this.availableProducts = [
      { id: 1, name: 'Apple', description: 'Apple Description', unitPrice: 250, quantity: 10, selected: false },
      { id: 2, name: 'Carrot', description: 'Carrot Description', unitPrice: 670, quantity: 20, selected: false },
      { id: 3, name: 'Rice', description: 'Rice Description', unitPrice: 200, quantity: 8, selected: false },
      { id: 4, name: 'Mushroom', description: 'Mushroom Description', unitPrice: 560, quantity: 30, selected: false },
      { id: 5, name: 'Onion', description: 'Onion Description', unitPrice: 100, quantity: 6, selected: false },
      { id: 6, name: 'Potatoe', description: 'Potatoe Description', unitPrice: 1000, quantity: 10, selected: false },
      { id: 7, name: 'Orange', description: 'Orange Description', unitPrice: 350, quantity: 4, selected: false }
    ];

    this.products = this.availableProducts.slice(0,2).filter(p => p.quantity > 0).map(p => ({ ...p, quantitySelected: p.quantity / 2 }));
  }

  loadData(): void {
    forkJoin({
      clients: this.clientService.getClientsBySellerId('4e5e0531-b49d-40c2-afbc-2e1772701431'),
    }).subscribe({
      next: (response) => {
        this.clients = response.clients;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('ORDER.CREATE_LOAD_DATA_ERROR_MESSAGE'),
          this.translate.instant('ORDER.CREATE_LOAD_DATA_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });
  }

  formatDate(date: Date): string {
    return date.toISOString().slice(0, 10);
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
    return this.products.reduce((total, prod) => total + prod.unitPrice * prod.quantitySelected, 0);
  }

  openModal() {
    this.selectedModalProducts = {};
    this.availableProducts.forEach(p => {
      const match = this.products.find(pr => pr.id === p.id);
      p.selected = !!match;
      
      if (p.selected) {
        this.selectedModalProducts[p.id] = match.quantitySelected || 1;
      }
    });
  }

  toggleSelectProduct(product: Product) {
    product.selected = !product.selected;
    if (product.selected) {
      this.selectedModalProducts[product.id] = product.quantity;
    } else {
      delete this.selectedModalProducts[product.id];
      this.removeProduct(product);
    }
  }

  increaseModalQuantity(productId: number) {
    if (this.selectedModalProducts[productId]) {
      this.selectedModalProducts[productId]++;
    }
  }

  decreaseModalQuantity(productId: number) {
    if (this.selectedModalProducts[productId] > 1) {
      this.selectedModalProducts[productId]--;
    }
  }

  addProductsToOrder() {
    Object.entries(this.selectedModalProducts).forEach(([id, quantity]) => {
      const pid = +id;
      const product = this.availableProducts.find(p => p.id === pid);
      if (product) {
        const existing = this.products.find(p => p.id === pid);
        if (existing) {
          existing.quantitySelected = quantity;
        } else {
          this.products.push({ ...product, quantitySelected: quantity });
        }
      }
    });
  }

  get paginatedModalProducts(): Product[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.availableProducts.slice(start, start + this.pageSize);
  }

  totalPages(): number {
    return Math.ceil(this.availableProducts.length / this.pageSize);
  }

  setPage(page: number) {
    if (page >= 1 && page <= this.totalPages()) {
      this.currentPage = page;
    }
  }

  createOrder() {
    const payload = {
      client_id: this.selectedClient,
      delivery_date: this.deliveryDate,
      payment_method: this.selectedPayment,
      products: this.products.map(p => ({
        product_id: p.id,
        units: p.quantity
      })),
    };
    console.log('Creating Order:', payload);
    // Aquí se puede integrar con un servicio de backend
  }
}
