import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { SellerService } from 'src/app/services/seller.service';
import { ToastrService } from 'ngx-toastr';
import { SellerDTO } from 'src/app/dtos/seller.dto';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-salespeople-register',
  templateUrl: './salespeople-register.component.html',
  styleUrls: ['./salespeople-register.component.css']
})
export class SalesPeopleRegisterComponent implements OnInit {
  sellerForm!: FormGroup;
  sellerZones: string[] = [
    'NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTER',
    'NORTHEAST', 'NORTHWEST', 'SOUTHEAST', 'SOUTHWEST'
  ];
  currencies: string[] = ['USD', 'COP', 'EUR', 'GBP', 'ARS'];

  constructor(
    private fb: FormBuilder,
    private sellerService: SellerService,
    private toastr: ToastrService,
    private router: Router,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
  }

  get formControls() {
    return this.sellerForm.controls;
  }

  initializeForm(): void {
    this.sellerForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(255)]],
      phone: ['', [Validators.required, Validators.maxLength(20), Validators.pattern(/^\+[0-9]+$/)]],
      email: ['', [Validators.required, Validators.email, Validators.minLength(10), Validators.maxLength(255)]],
      password: ['', [Validators.required, Validators.minLength(5), Validators.maxLength(50)]],
      confirmPassword: ['', Validators.required],
      zone: ['', Validators.required],
      quotaExpected: ['', [Validators.required, Validators.min(1)]],
      currencyQuota: ['', Validators.required],
      quarterlyTarget: ['', [Validators.required, Validators.min(1)]],
      currencyTarget: ['', Validators.required],
      performanceRecomendations: ['', Validators.required]
    }, { validator: this.passwordMatchValidator });
  }

  // Custom validator to ensure password and confirmPassword match
  passwordMatchValidator(form: AbstractControl) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { mismatch: true };
  }

  // Format a number with commas on blur
  formatNumber(controlName: string): void {
    const control = this.sellerForm.get(controlName);
    if (!control) return;
    let rawValue: string = control.value || '';
    rawValue = rawValue.replace(/,/g, '');  // Remove existing commas
    const numericValue = Number(rawValue);
    if (!isNaN(numericValue) && rawValue !== '') {
      control.setValue(numericValue.toLocaleString('en-US'), { emitEvent: false });
    }
  }

  registerSeller(formValue: any): void {
    if (this.sellerForm.invalid) return;

    // Remove commas and parse the quota fields
    const rawQuotaExpected = formValue.quotaExpected?.replace(/,/g, '') || '0';
    const rawQuarterlyTarget = formValue.quarterlyTarget?.replace(/,/g, '') || '0';

    const sellerData: SellerDTO = {
      name: formValue.name,
      phone: formValue.phone,
      email: formValue.email,
      password: formValue.password,
      type: 'SELLER',
      zone: formValue.zone,
      quota_expected: +rawQuotaExpected,
      currency_quota: formValue.currencyQuota,
      quartely_target: +rawQuarterlyTarget,
      currency_target: formValue.currencyTarget,
      performance_recomendations: formValue.performanceRecomendations
    };

    this.sellerService.createSeller(sellerData).subscribe({
      next: () => {
        this.toastr.success(
          this.translate.instant('SIGNUP.SUCCESS_MESSAGE'),
          this.translate.instant('SIGNUP.SUCCESS_TITLE'),
          { closeButton: true }
        );
        this.sellerForm.reset();
        
      },
      error: (err) => {
        this.toastr.error(
          this.translate.instant('SIGNUP.ERROR_MESSAGE') + ' ' + err.message,
          this.translate.instant('SIGNUP.ERROR_TITLE'),
          { closeButton: true }
        );
      }
    });
  }
}