import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { Product } from '../product';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from 'src/app/services/product.service';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {
  products: Array<Product> = [];

  constructor(
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService,
    private translate: TranslateService,
    private productService: ProductService,
  ) { }

  ngOnInit(): void {
    this.productService.getProducts().subscribe({
      next: (response) => {
        this.products = response;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.LIST_ERROR_TITLE'),
          this.translate.instant('PRODUCT.LIST_ERROR_MESSAGE'),
          { closeButton: true }
        );
      }
    });
  }

  editProduct(productId: string): void {
    this.routerPath.navigate(['/product/edit/' + productId]);
  }
}