import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { Product } from 'src/app/product/product';
import { ManufacturerPaginateDTO } from 'src/app/dtos/manufacturer';
import { ManufacturerService } from 'src/app/services/manufacturer.service';
import { ProductService } from 'src/app/services/product.service';
import { UtilPagination } from 'src/app/utils/util-pagination';

@Component({
  selector: 'app-manufacture-list-products',
  templateUrl: './manufacture-list-products.component.html',
  styleUrls: ['./manufacture-list-products.component.css']
})
export class ManufactureListProductsComponent implements OnInit {
  manufacturerId: string = '';
  manufacturerTotalItems = 0;
  manufacturerPaginated: ManufacturerPaginateDTO = {
    manufacturers: [],
    total: 0,
    page: 1,
    per_page: 10,
  }
  productPage = 1;
  productPerPage = 10;
  productTotalItems = 0;
  products: Product[] = [];

  constructor(
    private toastr: ToastrService,
    private readonly manufacturerService: ManufacturerService,
    private readonly productService: ProductService,
    private translate: TranslateService,
  ) { }

  ngOnInit(): void {
    this.listManufacturers();
  }

  listManufacturers(): void {
    this.manufacturerService.getManufacturersByList(
      this.manufacturerPaginated.page, this.manufacturerPaginated.per_page
    ).subscribe({
      next: (res) => {
        this.manufacturerPaginated = {
          manufacturers: res.manufacturers,
          total: res.total,
          page: res.page,
          per_page: res.per_page
        };
        this.manufacturerTotalItems = Math.ceil(res.total / res.per_page);
      },
      error: (err) => {
        this.toastr.error(
          this.translate.instant('MANUFACTURER_LIST.ERROR_LIST_MANUFACTURERS'),
          this.translate.instant('MANUFACTURER_LIST.ERROR_TITLE_MANUFACTURERS'),
        );
      }
    })
  }

  getProductsByManufacturerId(): void {
    if (this.manufacturerId != '') {
      this.productService.getProductsByManufactureId(
        this.productPage,
        this.productPerPage,
        this.manufacturerId,
      ).subscribe({
        next: (res) => {
          this.products = res;
          this.productTotalItems = res[0]?.total_items || 0;
        },
        error: (err) => {
          this.toastr.error(
            this.translate.instant('MANUFACTURER_LIST.ERROR_LIST_PRODUCTS'),
            this.translate.instant('MANUFACTURER_LIST.ERROR_TITLE_PRODUCTS'),
          );
        }
      })
    }
  }

  getPaginationManufacturersPages(current: number, total: number): (number | string)[] {
    return UtilPagination.getPages(current, total);
  }

  getPaginationProductsPages(current: number, total: number): (number | string)[] {
    return UtilPagination.getPages(current, total);
  }

  changeManufacturerPage(page: number): void {
    this.manufacturerPaginated.page += page;
    this.listManufacturers();
  }

  onClickManufacturerPage(page: number | string): void {
    const tempPage = Number(page);
    if (page !== this.manufacturerPaginated.page) {
      this.manufacturerPaginated.page = tempPage;
      this.listManufacturers();
    }
  }

  onSelectManufacturerCheckbox(id: string): void {
    if (this.manufacturerId === id) {
      this.manufacturerId = '';
      this.products = [];
      this.productPage = 1;
      this.productTotalItems = 0;
      return;
    }

    this.manufacturerId = id;
    this.getProductsByManufacturerId();
  }

  changeProductsPage(page: number): void {
    this.productPage += page;
    this.getProductsByManufacturerId();
  }

  onClickProductPage(page: number | string): void {
    const tempPage = Number(page);
    if (page !== this.productPage) {
      this.productPage = tempPage;
      this.getProductsByManufacturerId();
    }
  }
}
