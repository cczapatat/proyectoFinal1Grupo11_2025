import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { Manufacturer } from '../../dtos/manufacturer';
import { Product } from '../../product/product';
import { ProductService } from '../../services/product.service';
import { ManufacturerService } from '../../services/manufacturer.service';
import { AlarmService } from '../../services/alarm.service';
import { positiveNumberValidator } from 'src/app/validators/positive-number.validator';

@Component({
  selector: 'app-alarm-create',
  templateUrl: './alarm-create.component.html',
  styleUrls: ['./alarm-create.component.css']
})
export class AlarmCreateComponent implements OnInit {
  alarmForm: FormGroup;
  manufacturerList: Manufacturer[] = [];
  productList: Product[] = [];

  constructor(
    private formBuilder: FormBuilder,
    private toastr: ToastrService,
    private translate: TranslateService,
    private productService: ProductService,
    private manufacturerService: ManufacturerService,
    private alarmService: AlarmService
  ) {
    this.initializeForm();
  }

  ngOnInit(): void {
    this.loadManufacturers();
    this.setupFormListeners();
  }

  private initializeForm(): void {
    this.alarmForm = this.formBuilder.group({
      manufacture_id: ["", Validators.required],
      product_id: ["", Validators.required],
      is_set_min_value: [false],
      is_set_max_value: [false],
      minimum_value: [{ value: null, disabled: true }, [Validators.required, Validators.min(0)]],
      maximum_value: [{ value: null, disabled: true }, [Validators.required, positiveNumberValidator]],
      notes: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(255)]],
    }, { validators: this.atLeastOneValueSetValidator });

    this.alarmForm.reset();
  }

  private loadManufacturers(): void {
    this.manufacturerService.getManufacturerList().subscribe({
      next: (manufacturers) => {
        this.manufacturerList = manufacturers;
      },
      error: () => {
        this.showError(
          'ALARM.CREATE_LOAD_SERVICES_INFORMATION_MANUFACTURERS_ERROR_MESSAGE',
          'ALARM.CREATE_LOAD_SERVICES_INFORMATION_ERROR_TITLE'
        );
      }
    });
  }

  private setupFormListeners(): void {
    this.alarmForm.get('manufacture_id')?.valueChanges.subscribe(manufacturerId => {
      if (manufacturerId) {
        this.loadProducts(manufacturerId);
      } else {
        this.productList = [];
      }
    });

    this.setupToggleListener('is_set_min_value', 'minimum_value');
    this.setupToggleListener('is_set_max_value', 'maximum_value');
  }

  private loadProducts(manufacturerId: string): void {
    this.productService.getProductsByManufactureId(0, 50, manufacturerId).subscribe({
      next: (products) => {
        this.productList = products;
      },
      error: () => {
        this.showError(
          'ALARM.CREATE_LOAD_SERVICES_INFORMATION_PRODUCTS_ERROR_MESSAGE',
          'ALARM.CREATE_LOAD_SERVICES_INFORMATION_ERROR_TITLE'
        );
      }
    });
  }

  private setupToggleListener(toggleField: string, targetField: string): void {
    this.alarmForm.get(toggleField)?.valueChanges.subscribe((isChecked) => {
      const control = this.alarmForm.get(targetField);
      if (isChecked) {
        control?.enable();
      } else {
        control?.disable();
        control?.reset(null);
      }
    });
  }

  createAlarm(form: FormGroup): void {
    if (form.valid) {
      const formValues = form.value;
      const alarm = this.buildAlarmPayload(formValues);

      this.alarmService.createAlarm(alarm).subscribe({
        next: () => {
          this.showSuccess(
            'ALARM.CREATE_SUCCESS_MESSAGE',
            'ALARM.CREATE_SUCCESS_TITLE'
          );
          this.alarmForm.reset();
        },
        error: () => {
          this.showError(
            'ALARM.CREATE_ERROR_MESSAGE',
            'ALARM.CREATE_ERROR_TITLE'
          );
        }
      });
    }
  }

  private buildAlarmPayload(formValues: any): any {
    const alarm: any = {
      manufacture_id: formValues.manufacture_id,
      product_id: formValues.product_id,
      notes: formValues.notes
    };

    if (formValues.is_set_min_value) {
      alarm.minimum_value = Number(formValues.minimum_value);
    }

    if (formValues.is_set_max_value) {
      alarm.maximum_value = Number(formValues.maximum_value);
    }

    return alarm;
  }

  private atLeastOneValueSetValidator: ValidatorFn = (formGroup: AbstractControl): ValidationErrors | null => {
    const minValue = formGroup.get('minimum_value')?.value;
    const maxValue = formGroup.get('maximum_value')?.value;

    if (!minValue && !maxValue) {
      return { atLeastOneValueRequired: true };
    }
    return null;
  };

  private showError(messageKey: string, titleKey: string): void {
    this.toastr.error(
      this.translate.instant(messageKey),
      this.translate.instant(titleKey),
      { closeButton: true }
    );
  }

  private showSuccess(messageKey: string, titleKey: string): void {
    this.toastr.success(
      this.translate.instant(messageKey),
      this.translate.instant(titleKey),
      { closeButton: true }
    );
  }
}