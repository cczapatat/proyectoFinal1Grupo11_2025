import { Component, OnInit } from '@angular/core';
import { StoreService } from 'src/app/services/store.service';
import { ProductService } from 'src/app/services/product.service';
import { StocksService } from 'src/app/services/stocks.service';
import { ToastrService } from 'ngx-toastr';
import { TranslateService } from '@ngx-translate/core';
import { PaginatedStores, StoreDto } from 'src/app/dtos/store.dto';
import { ProductDto as Product, PaginatedProducts } from 'src/app/dtos/product';
import { AssignedStockDto } from 'src/app/dtos/assignedStock';

interface ProductExtended extends Product {
  selected?: boolean;
  quantity?: number;
  local_image?: string;
}

interface ExtendedStore extends StoreDto {
  image: string;
}

@Component({
  selector: 'app-store-assign-product',
  templateUrl: './store-assign-product.component.html',
  styleUrls: ['./store-assign-product.component.css']
})
export class StoreAssignProductComponent implements OnInit {
  // Extended stores and products loaded via service calls.
  stores: ExtendedStore[] = [];
  products: ProductExtended[] = [];

  // Dictionary to persist product selections across pagination.
  productSelections: { [id: string]: { selected: boolean, quantity: number } } = {};

  // Currently selected store.
  selectedStore: ExtendedStore | null = null;

  // Pagination and sorting settings for stores.
  storePage: number = 1;
  totalStorePages: number = 1;
  storeSortOrder: string = 'asc';

  // Pagination and sorting settings for products.
  productPage: number = 1;
  totalProductPages: number = 1;
  productSortOrder: string = 'asc';

  // Flags for showing/hiding filter textbox.
  showStoreFilter: boolean = false;
  showProductFilter: boolean = false;

  // Flag to track unsaved changes.
  hasChanges: boolean = false;

  constructor(
    private storeService: StoreService,
    private productService: ProductService,
    private stocksService: StocksService,
    private toastr: ToastrService,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.loadStores(this.storePage);
    this.loadProducts(this.productPage);
  }

  /**
   * Transforms a store name into an image filename.
   * For example, "Grupo Éxito" becomes "grupo_éxito.png".
   */
  private transformStoreName(name: string): string {
    return name.toLowerCase().trim().replace(/\s+/g, '_') + '.png';
  }

  /**
   * Transforms a product name into a local image filename.
   * For example, "Chocolate Bar" becomes "chocolate_bar.png".
   */
  private transformProductName(name: string): string {
    return name.toLowerCase().trim().replace(/\s+/g, '_') + '.png';
  }

  /**
   * Loads paginated stores using StoreService.
   * Each store is extended with an "image" property.
   */
  loadStores(page: number): void {
    this.storeService.getPaginatedStores(page, 10, this.storeSortOrder)
      .subscribe((response) => {
        this.stores = response.data.map(store => ({
          ...store,
          image: this.transformStoreName(store.name)
        }));
        this.storePage = response.page;
        this.totalStorePages = response.total_pages;
      }, error => {
        console.error('Error loading stores:', error);
        this.toastr.error(this.translate.instant('STORE.LOAD_ERROR'));
      });
  }

  /**
   * Loads paginated products using ProductService.
   * Each product is extended with a "local_image" property and merged with persisted selections.
   */
  loadProducts(page: number): void {
    this.productService.getProductsPaginated(page, 10, this.productSortOrder)
      .subscribe((response) => {
        const newProducts: ProductExtended[] = response.data.map(p => {
          const selection = this.productSelections[p.id] || { selected: false, quantity: 0 };
          return {
            ...p,
            selected: selection.selected,
            quantity: selection.quantity,
            local_image: this.transformProductName(p.name)
          };
        });
        this.products = newProducts;
        this.productPage = response.page;
        this.totalProductPages = response.total_pages;
      }, error => {
        console.error('Error loading products:', error);
        this.toastr.error(this.translate.instant('PRODUCT.LOAD_ERROR'));
      });
  }

  // Toggle store sort order.
  toggleStoreSortOrder(): void {
    this.storeSortOrder = this.storeSortOrder === 'asc' ? 'desc' : 'asc';
    this.loadStores(this.storePage);
  }

  // Toggle product sort order.
  toggleProductSortOrder(): void {
    this.productSortOrder = this.productSortOrder === 'asc' ? 'desc' : 'asc';
    this.loadProducts(this.productPage);
  }

  /**
   * Handles selection of a store.
   * When a store is selected, loads its assigned product stocks.
   */
  onSelectStore(store: ExtendedStore): void {
    if (this.selectedStore && this.selectedStore.id === store.id) {
      this.selectedStore = null;
      this.resetProductSelections();
    } else {
      this.selectedStore = store;
      this.resetProductSelections();
      this.stocksService.getStocksByStore(store.id)
        .subscribe(response => {
          const assignedStocks = response.stocks;
          this.products.forEach(product => {
            const assignment = assignedStocks.find((s: any) => s.product_id === product.id);
            if (assignment) {
              product.selected = true;
              product.quantity = assignment.assigned_stock;
              this.productSelections[product.id] = { selected: true, quantity: assignment.assigned_stock };
            } else {
              product.selected = false;
              product.quantity = 0;
              this.productSelections[product.id] = { selected: false, quantity: 0 };
            }
          });
          this.hasChanges = false;
        }, error => {
          console.error('Error retrieving assigned stocks:', error);
          this.toastr.error(this.translate.instant('STORE.STOCKS_LOAD_ERROR'));
        });
    }
  }

  /**
   * Resets product selections and clears the persistent dictionary.
   */
  resetProductSelections(): void {
    this.products.forEach(product => {
      product.selected = false;
      product.quantity = 0;
      this.productSelections[product.id] = { selected: false, quantity: 0 };
    });
    this.hasChanges = false;
  }

  /**
   * Handles changes in product selection.
   */
  onProductSelect(product: ProductExtended): void {
    product.selected = !product.selected;
    if (!product.selected) {
      product.quantity = 0;
    }
    this.productSelections[product.id] = { selected: product.selected || false, quantity: product.quantity || 0 };
    this.hasChanges = true;
  }

  /**
   * Handles changes in product quantity.
   */
  onProductQuantityChange(product: ProductExtended): void {
    if (product.quantity < 0) {
      product.quantity = 0;
    }
    this.productSelections[product.id] = { selected: product.selected || false, quantity: product.quantity || 0 };
    this.hasChanges = true;
  }

  /**
   * Generates an array of page numbers for store pagination.
   */
  getPaginationStorePages(currentPage: number, totalPages: number): number[] {
    const pages: number[] = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  /**
   * Generates an array of page numbers for product pagination.
   */
  getPaginationProductPages(currentPage: number, totalPages: number): number[] {
    const pages: number[] = [];
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

  // Change product page. Persist selections before loading new products.
  changeProductPage(delta: number): void {
    this.products.forEach(product => {
      this.productSelections[product.id] = { selected: product.selected || false, quantity: product.quantity || 0 };
    });
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
    this.products.forEach(product => {
      this.productSelections[product.id] = { selected: product.selected || false, quantity: product.quantity || 0 };
    });
    this.productPage = page;
    this.loadProducts(this.productPage);
  }

  /**
   * Constructs an AssignedStockDto and saves the assignments.
   * After a successful save, it unselects all items in both tables.
   */
  saveAssignments(): void {
    if (!this.selectedStore) {
      this.toastr.warning(this.translate.instant('STORE.PLEASE_SELECT_STORE'));
      return;
    }
    if (!this.hasChanges) {
      this.toastr.info(this.translate.instant('STORE.NO_CHANGES'));
      return;
    }
    const stocks = this.products
      .filter(product => product.selected)
      .map(product => ({
        product_id: product.id,
        assigned_stock: product.quantity,
        id: '' // Empty indicates a new assignment.
      }));
    const dto: AssignedStockDto = {
      store_id: this.selectedStore.id as string,
      stocks: stocks
    };
    this.stocksService.assignStockToStore(dto)
      .subscribe(response => {
        this.hasChanges = false;
        this.toastr.success(this.translate.instant('STORE.ASSIGN_SUCCESS'));
        // Unselect all items.
        this.selectedStore = null;
        this.resetProductSelections();
      }, error => {
        console.error('Error saving assignments:', error);
        this.toastr.error(this.translate.instant('STORE.ASSIGN_ERROR'));
      });
  }
}