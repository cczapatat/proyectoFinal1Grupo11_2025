import { Component, OnInit } from '@angular/core';
import { StoreService } from 'src/app/services/store.service';
import { ProductService } from 'src/app/services/product.service';
import { StocksService } from 'src/app/services/stocks.service';
import { PaginatedStores, StoreDto } from 'src/app/dtos/store.dto';
import { ProductDto as Product, PaginatedProducts } from 'src/app/dtos/product';
import { AssignedStockDto } from 'src/app/dtos/assignedStock';

interface ProductExtended extends Product {
  selected?: boolean;
  quantity?: number;
}

@Component({
  selector: 'app-store-assign-product',
  templateUrl: './store-assign-product.component.html',
  styleUrls: ['./store-assign-product.component.css']
})
export class StoreAssignProductComponent implements OnInit {
  // Arrays for stores and products loaded via service calls.
  stores: StoreDto[] = [];
  products: ProductExtended[] = [];

  // Currently selected store
  selectedStore: StoreDto | null = null;

  // Pagination and sorting settings for stores.
  storePage: number = 1;
  totalStorePages: number = 1;
  storeSortOrder: string = 'asc';

  // Pagination and sorting settings for products.
  productPage: number = 1;
  totalProductPages: number = 1;
  productSortOrder: string = 'asc';

  // Flags to control filter textbox visibility.
  showStoreFilter: boolean = false;
  showProductFilter: boolean = false;

  // Flag to track unsaved changes.
  hasChanges: boolean = false;

  constructor(
    private storeService: StoreService,
    private productService: ProductService,
    private stocksService: StocksService
  ) {}

  ngOnInit(): void {
    this.loadStores(this.storePage);
    this.loadProducts(this.productPage);
  }

  /**
   * Loads paginated stores using StoreService.
   */
  loadStores(page: number): void {
    this.storeService.getPaginatedStores(page, 10, this.storeSortOrder)
      .subscribe((response: PaginatedStores) => {
        this.stores = response.data;
        this.storePage = response.page;
        this.totalStorePages = response.total_pages;
      }, error => {
        console.error('Error loading stores:', error);
      });
  }

  /**
   * Loads paginated products using ProductService.
   * It merges the new data with any existing selection.
   */
  loadProducts(page: number): void {
    this.productService.getProductsPaginated(page, 10, this.productSortOrder)
      .subscribe((response: PaginatedProducts) => {
        const newProducts: ProductExtended[] = response.data.map(p => {
          const extended: ProductExtended = {
            ...p,
            selected: false,
            quantity: 0
          };
          const existing = this.products.find(ep => ep.id === p.id);
          if (existing) {
            extended.selected = existing.selected || false;
            extended.quantity = existing.quantity || 0;
          }
          return extended;
        });
        this.products = newProducts;
        this.productPage = response.page;
        this.totalProductPages = response.total_pages;
      }, error => {
        console.error('Error loading products:', error);
      });
  }

  // Toggle store sort order and reload stores.
  toggleStoreSortOrder(): void {
    this.storeSortOrder = this.storeSortOrder === 'asc' ? 'desc' : 'asc';
    this.loadStores(this.storePage);
  }

  // Toggle product sort order and reload products.
  toggleProductSortOrder(): void {
    this.productSortOrder = this.productSortOrder === 'asc' ? 'desc' : 'asc';
    this.loadProducts(this.productPage);
  }

  /**
   * Handles selection of a store. Only one store can be selected at a time.
   * When a store is selected, loads its assigned product stocks.
   */
  onSelectStore(store: StoreDto): void {
    if (this.selectedStore && this.selectedStore.id === store.id) {
      this.selectedStore = null;
      this.resetProductSelections();
    } else {
      this.selectedStore = store;
      this.resetProductSelections();
      this.stocksService.getStocksByStore(store.id)
        .subscribe(response => {
          // Expected response shape: { store_id: string, stocks: AssignedStock[] }
          const assignedStocks = response.stocks;
          this.products.forEach(product => {
            const assignment = assignedStocks.find((s: any) => s.product_id === product.id);
            if (assignment) {
              product.selected = true;
              product.quantity = assignment.assigned_stock;
            } else {
              product.selected = false;
              product.quantity = 0;
            }
          });
          this.hasChanges = false;
        }, error => {
          console.error('Error retrieving assigned stocks:', error);
        });
    }
  }

  /**
   * Resets all product selections and quantities.
   */
  resetProductSelections(): void {
    this.products.forEach(product => {
      product.selected = false;
      product.quantity = 0;
    });
    this.hasChanges = false;
  }

  /**
   * Toggles product selection.
   */
  onProductSelect(product: ProductExtended): void {
    product.selected = !product.selected;
    if (!product.selected) {
      product.quantity = 0;
    }
    this.hasChanges = true;
  }

  /**
   * Generates an array of page numbers for store pagination.
   */
  getPaginationStorePages(currentPage: number, totalPages: number): number[] {
    let pages: number[] = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  /**
   * Generates an array of page numbers for product pagination.
   */
  getPaginationProductPages(currentPage: number, totalPages: number): number[] {
    let pages: number[] = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  // Change store page.
  changeStorePage(delta: number): void {
    const newPage = this.storePage + delta;
    if (newPage >= 1 && newPage <= this.totalStorePages) {
      this.storePage = newPage;
      this.loadStores(this.storePage);
    }
  }

  // Change product page.
  changeProductPage(delta: number): void {
    const newPage = this.productPage + delta;
    if (newPage >= 1 && newPage <= this.totalProductPages) {
      this.productPage = newPage;
      this.loadProducts(this.productPage);
    }
  }

  onStorePageClick(page: number): void {
    this.storePage = page;
    this.loadStores(this.storePage);
  }

  onProductPageClick(page: number): void {
    this.productPage = page;
    this.loadProducts(this.productPage);
  }

  /**
   * Constructs an AssignedStockDto from the current selections and saves the assignments.
   */
  saveAssignments(): void {
    if (!this.selectedStore) {
      alert('Please select a store first.');
      return;
    }
    if (!this.hasChanges) {
      alert('No changes to save.');
      return;
    }
    const stocks = this.products
      .filter(product => product.selected)
      .map(product => ({
        product_id: product.id,
        assigned_stock: product.quantity,
        id: ''  // Empty ID indicates a new assignment
      }));
    const dto: AssignedStockDto = {
      store_id: this.selectedStore.id as string,
      stocks: stocks
    };
    this.stocksService.assignStockToStore(dto).subscribe(response => {
      this.hasChanges = false;
      alert('Assignments saved successfully.');
    }, error => {
      console.error('Error saving assignments:', error);
      alert('Error saving assignments.');
    });
  }
}