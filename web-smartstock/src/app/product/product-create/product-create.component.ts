import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { Manufacturer } from '../manufacturer';
import { Router } from '@angular/router';
import { ProductService } from '../product.service';
import { ManufacturerService } from '../manufacturer.service';
import { Product } from '../product';
import { positiveNumberValidator } from 'src/app/validators/positive-number.validator';
import { fa } from '@faker-js/faker';
import { ProductCategory } from '../product-category';
import { ProductCurrency } from '../product-currency';

@Component({
  selector: 'app-product-create',
  templateUrl: './product-create.component.html',
  styleUrls: ['./product-create.component.css']
})
export class ProductCreateComponent implements OnInit {
  productForm: FormGroup;  
  manufacturerList: Manufacturer[] = [];
  categories: ProductCategory[] = [];
  currencies: ProductCurrency[] = [];
  minDate: String = "";
  today = new Date();
  tomorrow = new Date(this.today);

  constructor(
    private formBuilder: FormBuilder,
    private routerPath: Router,
    private toastr: ToastrService,
    private translate: TranslateService,
    private productService: ProductService,
    private manufacturerService: ManufacturerService
  ) { 
    this.productForm = this.formBuilder.group({
      manufacturer_id: ["", Validators.required],
      name: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
      description: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
      category: ["", Validators.required],
      unit_price: ["", [Validators.required, positiveNumberValidator]],
      currency_price: ["", Validators.required],
      is_promotion: [false],
      discount_price: [{ value: "", disabled: true }, [Validators.required, positiveNumberValidator]],
      expired_at: [null],
      url_photo: ["", [Validators.required, Validators.pattern("^(https?:\/\/)?([\\da-z.-]+)\\.([a-z.]{2,6})([\/\\w .-]*)*\/?$")]],
      store_conditions: ["", Validators.required]
    });

    this.productForm.reset();
  }

  ngOnInit() {
    this.tomorrow.setDate(this.today.getDate() + 1);
    this.minDate = this.tomorrow.toISOString().split('T')[0];
    this.manufacturerService.getManufacturerList().subscribe({
      next: (manufacturers) => {
        this.manufacturerList = manufacturers;

        this.productForm = this.formBuilder.group({
          manufacturer_id: ["", Validators.required],
          name: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
          description: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
          category: ["", Validators.required],
          unit_price: ["", [Validators.required, positiveNumberValidator]],
          currency_price: ["", Validators.required],
          is_promotion: [false],
          discount_price: [{ value: "", disabled: true }, [Validators.required, positiveNumberValidator]],
          expired_at: [null],
          url_photo: ["", [Validators.required, Validators.pattern("^(https?:\/\/)?([\\da-z.-]+)\\.([a-z.]{2,6})([\/\\w .-]*)*\/?$")]],
          store_conditions: ["", Validators.required]
        });
  
        this.productForm.get('is_promotion')?.valueChanges.subscribe((isPromotion) => {
          const discountPriceControl = this.productForm.get('discount_price');
          if (isPromotion) {
            discountPriceControl?.enable();
          } else {
            discountPriceControl?.disable();
            discountPriceControl?.reset();
          }
        });
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.CREATE_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
          this.translate.instant('PRODUCT.CREATE_MANUFACTURES_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });

    this.productService.getProductCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.CREATE_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
          this.translate.instant('PRODUCT.CREATE_CATEGORIES_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });

    this.productService.getProductCurrencies().subscribe({
      next: (currencies) => {
        this.currencies = currencies;
      }
      , error: (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.CREATE_LOAD_SERVICES_INFORMARION_ERROR_TITLE'),
          this.translate.instant('PRODUCT.CREATE_CURRENCIES_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });
  }

  createProduct(product: Product): void {
    if (this.productForm.valid) {
      this.productService.createProduct(product).subscribe((product) => {
        this.toastr.success(
          this.translate.instant('PRODUCT.CREATE_SUCCESS_MESSAGE'),
          this.translate.instant('PRODUCT.CREATE_SUCCESS_TITLE'),
          { closeButton: true },
        );
        this.productForm.reset();
      }, (error) => {
        this.toastr.error(
          this.translate.instant('PRODUCT.CREATE_ERROR_MESSAGE'),
          this.translate.instant('PRODUCT.CREATE_ERROR_TITLE'),
        );
        console.error(error);
      });
    }
  }

  cancelProduct(): void {
    this.productForm.reset();
    this.routerPath.navigate(['/product']);
  }
}
