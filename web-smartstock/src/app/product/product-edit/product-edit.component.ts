import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { Product } from '../product';
import { Form, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Manufacturer } from 'src/app/dtos/manufacturer';
import { ProductCategory } from 'src/app/dtos/product-category';
import { ProductCurrency } from 'src/app/dtos/product-currency';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from 'src/app/services/product.service';
import { ManufacturerService } from 'src/app/services/manufacturer.service';
import { TranslateService } from '@ngx-translate/core';
import { positiveNumberValidator } from 'src/app/validators/positive-number.validator';

@Component({
  selector: 'app-product-edit',
  templateUrl: './product-edit.component.html',
  styleUrls: ['./product-edit.component.css']
})
export class ProductEditComponent implements OnInit {
  product: Product
  productForm: FormGroup = {} as FormGroup;
  manufacturerList: Manufacturer[] = [];
  categories: ProductCategory[] = [];
  currencies: ProductCurrency[] = [];
  productId: string | null = null;
  minDate: String = "";
  today = new Date();
  tomorrow = new Date(this.today);

  constructor(
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService,
    private translate: TranslateService,
    private productService: ProductService,
    private manufacturerService: ManufacturerService
  ) {
    this.tomorrow.setDate(this.today.getDate() + 1);
    this.minDate = this.tomorrow.toISOString().split('T')[0];

    this.productForm = this.formBuilder.group({
      manufacturer_id: ["", Validators.required],
      name: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
      description: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
      category: ["", Validators.required],
      unit_price: ["", [Validators.required, positiveNumberValidator]],
      currency_price: ["", Validators.required],
      is_promotion: [false],
      discount_price: [{ value: 0, disabled: true }, [Validators.required, positiveNumberValidator]],
      expired_at: [""],
      url_photo: ["", [Validators.required, Validators.pattern("^(https?:\/\/)?([\\da-z.-]+)\\.([a-z.]{2,6})([\/\\w .-]*)*\/?$")]],
      store_conditions: ["", Validators.required]
    });

    this.productForm.get('is_promotion')?.valueChanges.subscribe((isPromotion) => {
      const discountPriceControl = this.productForm.get('discount_price');
      if (isPromotion) {
        discountPriceControl?.enable();
      } else {
        this.productForm.patchValue({ discount_price: 0 });
        discountPriceControl?.disable();
        discountPriceControl?.reset();
      }
    });
  }

  ngOnInit(): void {
    this.productId = this.router.snapshot.paramMap.get('id');

    this.productService.getProductCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.EDIT_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
          this.translate.instant('PRODUCT.EDIT_CATEGORY_ERROR_MESSAGE'),
          { closeButton: true }
        );
      }
    });

    this.productService.getProductCurrencies().subscribe({
      next: (currencies) => {
        this.currencies = currencies;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.EDIT_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
          this.translate.instant('PRODUCT.EDIT_CURRENCY_ERROR_MESSAGE'),
          { closeButton: true }
        );
      }
    });
    this.manufacturerService.getManufacturerList().subscribe({
      next: (manufacturers) => {
        this.manufacturerList = manufacturers;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.EDIT_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
          this.translate.instant('PRODUCT.EDIT_MANUFACTURES_ERROR_MESSAGE'),
          { closeButton: true }
        );
      }
    });

    if (this.productId) {
      this.productService.getProductById(this.productId).subscribe({
        next: (product) => {
          this.product = product;

          this.productForm.patchValue({
            manufacturer_id: product.manufacturer_id,
            name: product.name,
            description: product.description,
            category: product.category,
            unit_price: product.unit_price,
            currency_price: product.currency_price,
            is_promotion: product.is_promotion,
            discount_price: product.discount_price ? product.discount_price : 0,
            expired_at: product.expired_at ? new Date(product.expired_at).toISOString().split('T')[0] : "",
            url_photo: product.url_photo,
            store_conditions: product.store_conditions
          });
        },
        error: (error) => {
          this.toastr.error(
            this.translate.instant('PRODUCT.EDIT_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
            this.translate.instant('PRODUCT.EDIT_PRODUCT_ERROR_MESSAGE'),
            { closeButton: true }
          );
        }
      });
    }
  }

  editProduct(product: Product) {
    product.discount_price = product.discount_price ?? 0;

    this.productService.updateProduct(this.productId, product).subscribe({
      next: (response) => {
        this.toastr.success(
          this.translate.instant('PRODUCT.EDIT_SUCCESS_TITLE'),
          this.translate.instant('PRODUCT.EDIT_SUCCESS_MESSAGE'),
          { closeButton: true }
        );
        
        this.routerPath.navigate(['/product']);
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.EDIT_ERROR_TITLE'),
          this.translate.instant('PRODUCT.EDIT_ERROR_MESSAGE'),
          { closeButton: true }
        );
      }
    });
  }
}