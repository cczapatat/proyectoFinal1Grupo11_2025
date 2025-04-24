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
  stock_id?: string;
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
  // Tiendas extendidas y productos cargados a través de llamadas a servicios.
  stores: ExtendedStore[] = [];
  products: ProductExtended[] = [];

  // Diccionario para persistir las selecciones de productos entre paginaciones.
  productSelections: { [id: string]: { selected: boolean, quantity: number, stock_id : string } } = {};

  // Tienda actualmente seleccionada.
  selectedStore: ExtendedStore | null = null;

  // Configuración de paginación y ordenamiento para tiendas.
  storePage: number = 1;
  totalStorePages: number = 1;
  storeSortOrder: string = 'asc';

  // Configuración de paginación y ordenamiento para productos.
  productPage: number = 1;
  totalProductPages: number = 1;
  productSortOrder: string = 'asc';

  // Flags para mostrar/ocultar el cuadro de texto de filtro.
  showStoreFilter: boolean = false;
  showProductFilter: boolean = false;

  // Flag para rastrear cambios no guardados.
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
   * Transforma el nombre de una tienda en un nombre de archivo de imagen.
   * Por ejemplo, "Grupo Éxito" se convierte en "grupo_éxito.png".
   */
  private transformStoreName(name: string): string {
    return name.toLowerCase().trim().replace(/\s+/g, '_') + '.png';
  }

  /**
   * Transforma el nombre de un producto en un nombre de archivo de imagen local.
   * Por ejemplo, "Chocolate Bar" se convierte en "chocolate_bar.png".
   */
  private transformProductName(name: string): string {
    return name.toLowerCase().trim().replace(/\s+/g, '_') + '.png';
  }

  /**
   * Carga tiendas paginadas usando StoreService.
   * Cada tienda se extiende con una propiedad "image".
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
        console.error('Error al cargar tiendas:', error);
        this.toastr.error(this.translate.instant('STORE.LOAD_ERROR'));
      });
  }

  /**
   * Carga productos paginados usando ProductService.
   * Cada producto se extiende con una propiedad "local_image" y se fusiona con selecciones persistidas.
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
        console.error('Error al cargar productos:', error);
        this.toastr.error(this.translate.instant('PRODUCT.LOAD_ERROR'));
      });
  }

  // Alterna el orden de clasificación de las tiendas.
  toggleStoreSortOrder(): void {
    this.storeSortOrder = this.storeSortOrder === 'asc' ? 'desc' : 'asc';
    this.loadStores(this.storePage);
  }

  // Alterna el orden de clasificación de los productos.
  toggleProductSortOrder(): void {
    this.productSortOrder = this.productSortOrder === 'asc' ? 'desc' : 'asc';
    this.loadProducts(this.productPage);
  }

  /**
   * Maneja la selección de una tienda.
   * Cuando se selecciona una tienda, carga los stocks de productos asignados.
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
              
              this.productSelections[product.id] = { selected: true, quantity: assignment.assigned_stock, stock_id: assignment.id };
              console.log(this.productSelections);
            } else {
              product.selected = false;
              product.quantity = 0;
              this.productSelections[product.id] = { selected: false, quantity: 0, stock_id: ""  };
            }
          });
          this.hasChanges = false;
        }, error => {
          console.error('Error al recuperar stocks asignados:', error);
          this.toastr.error(this.translate.instant('STORE.STOCKS_LOAD_ERROR'));
        });
    }
  }

  /**
   * Restablece las selecciones de productos y limpia el diccionario persistente.
   */
  resetProductSelections(): void {
    this.products.forEach(product => {
      product.selected = false;
      product.quantity = 0;
      this.productSelections[product.id] = { selected: false, quantity: 0, stock_id: "" };
    });
    this.hasChanges = false;
  }

  /**
   * Maneja los cambios en la selección de productos.
   */
  onProductSelect(product: ProductExtended): void {
    product.selected = !product.selected;
    if (!product.selected) {
      product.quantity = 0;
    }
    this.productSelections[product.id] = { 
      selected: product.selected || false, 
      quantity: product.quantity || 0, 
      stock_id: this.productSelections[product.id]?.stock_id || '' 
    };
    this.hasChanges = true;
  }

  /**
   * Maneja los cambios en la cantidad de productos.
   */
  onProductQuantityChange(product: ProductExtended): void {
    if (product.quantity < 0) {
      product.quantity = 0;
    }
    this.productSelections[product.id] = { 
      selected: product.selected || false, 
      quantity: product.quantity || 0, 
      stock_id: this.productSelections[product.id]?.stock_id || '' 
    };
    this.hasChanges = true;
  }

  /**
   * Genera un array de números de página para la paginación de tiendas.
   */
  getPaginationStorePages(currentPage: number, totalPages: number): number[] {
    const pages: number[] = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  /**
   * Genera un array de números de página para la paginación de productos.
   */
  getPaginationProductPages(currentPage: number, totalPages: number): number[] {
    const pages: number[] = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  // Cambia la página de tiendas.
  changeStorePage(delta: number): void {
    const newPage = this.storePage + delta;
    if (newPage >= 1 && newPage <= this.totalStorePages) {
      this.storePage = newPage;
      this.loadStores(this.storePage);
    }
  }

  // Cambia la página de productos. Persiste las selecciones antes de cargar nuevos productos.
  changeProductPage(delta: number): void {
    this.products.forEach(product => {
      this.productSelections[product.id] = { selected: product.selected || false, quantity: product.quantity || 0, stock_id: this.productSelections[product.id].stock_id };
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
      this.productSelections[product.id] = { selected: product.selected || false, quantity: product.quantity || 0, stock_id: this.productSelections[product.id].stock_id };
    });
    this.productPage = page;
    this.loadProducts(this.productPage);
  }

  /**
   * Construye un AssignedStockDto y guarda las asignaciones.
   * Después de un guardado exitoso, deselecciona todos los elementos en ambas tablas.
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
      id: this.productSelections[product.id]?.stock_id || ''
      }));

    const dto: AssignedStockDto = {
      store_id: this.selectedStore.id as string,
      stocks: stocks
    };
    this.stocksService.assignStockToStore(dto)
      .subscribe(response => {
        this.hasChanges = false;
        this.toastr.success(this.translate.instant('STORE.ASSIGN_SUCCESS'));
        // Deselecciona todos los elementos.
        this.selectedStore = null;
        this.resetProductSelections();
      }, error => {
        console.error('Error al guardar asignaciones:', error);
        this.toastr.error(this.translate.instant('STORE.ASSIGN_ERROR'));
      });
  }
}