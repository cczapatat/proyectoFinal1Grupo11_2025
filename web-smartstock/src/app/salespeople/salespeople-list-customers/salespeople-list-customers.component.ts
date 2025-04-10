import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

interface Salesperson {
  id: number;
  name: string;
  email: string;
  zone: string;
  imageUrl: string;
}

interface Customer {
  id: number;
  name: string;
  email: string;
  zone: string;
  imageUrl: string;
}

@Component({
  selector: 'app-salespeople-list-customers',
  templateUrl: './salespeople-list-customers.component.html',
  styleUrls: ['./salespeople-list-customers.component.css']
})
export class SalespeopleListCustomersComponent implements OnInit {
  constructor(private toastr: ToastrService) {}
  salespeople: Salesperson[] = [];
  displayedSalespeople: Salesperson[] = [];
  customers: Customer[] = [];
  displayedCustomers: Customer[] = [];

  selectedSalespersonId: number | null = null;

  salespersonPage = 1;
  customerPage = 1;
  readonly pageSize = 10;

  ngOnInit(): void {
    this.getSalespeople();
  }

  getSalespeople() {
    // Simulated network request (replace with your backend API)
    this.salespeople = Array.from({ length: 25 }, (_, i) => ({
      id: i + 1,
      name: `Salesperson ${i + 1}`,
      email: `sales${i + 1}@company.com`,
      zone: `Zone ${i % 3 + 1}`,
      imageUrl: 'https://via.placeholder.com/40'
    }));
    this.updateDisplayedSalespeople();
  }

  getCustomersBySalespersonId(salespersonId: number) {
    // Simulated network request (replace with your backend API)
    this.customers = Array.from({ length: 28 }, (_, i) => ({
      id: i + 1,
      name: `Customer ${i + 1}`,
      email: `cust${i + 1}@client.com`,
      zone: `Zone ${i % 4 + 1}`,
      imageUrl: 'https://via.placeholder.com/40'
    }));
    this.customerPage = 1;
    this.updateDisplayedCustomers();
  }

  updateDisplayedSalespeople() {
    const start = (this.salespersonPage - 1) * this.pageSize;
    this.displayedSalespeople = this.salespeople.slice(start, start + this.pageSize);
  }

  updateDisplayedCustomers() {
    const start = (this.customerPage - 1) * this.pageSize;
    this.displayedCustomers = this.customers.slice(start, start + this.pageSize);
  }

  selectSalesperson(id: number) {
    if (this.selectedSalespersonId === id) {
      // Deselect
      this.selectedSalespersonId = null;
      this.customers = [];
      this.displayedCustomers = [];
    } else {
      this.selectedSalespersonId = id;
      this.getCustomersBySalespersonId(id);
    }
  }

  // Pagination navigation
  goToSalespersonPage(page: number) {
    this.salespersonPage = page;
    this.updateDisplayedSalespeople();
  }

  goToCustomerPage(page: number) {
    this.customerPage = page;
    this.updateDisplayedCustomers();
  }

  getSalespersonTotalPages(): number {
    return Math.ceil(this.salespeople.length / this.pageSize);
  }

  getCustomerTotalPages(): number {
    return Math.ceil(this.customers.length / this.pageSize);
  }

  generatePageArray(totalPages: number): number[] {
    const pages: number[] = [];
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      const current = this.selectedSalespersonId ? this.customerPage : this.salespersonPage;
      if (current <= 4) {
        pages.push(1, 2, 3, 4, 5, -1, totalPages);
      } else if (current >= totalPages - 3) {
        pages.push(1, -1, totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
      } else {
        pages.push(1, -1, current - 1, current, current + 1, -1, totalPages);
      }
    }
    return pages;
  }
}
