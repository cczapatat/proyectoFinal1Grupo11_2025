import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { SellerService } from 'src/app/services/seller.service';
import { ToastrService } from 'ngx-toastr';
import { SellerDTO } from 'src/app/dtos/seller.dto';

@Component({
  selector: 'app-user-session-sign-up',
  templateUrl: './user-session-sign-up.component.html',
  styleUrls: ['./user-session-sign-up.component.css']
})
export class UserSessionSignUpComponent implements OnInit {
  sellerForm!: FormGroup;
  sellerZones: string[] = [
    'NORTH','SOUTH','EAST','WEST','CENTER',
    'NORTHEAST','NORTHWEST','SOUTHEAST','SOUTHWEST'
  ];
  currencies: string[] = ['USD','COP','EUR','GBP','ARS'];

  constructor(
    private fb: FormBuilder,
    private sellerService: SellerService,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
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

  // Ensures password and confirmPassword match
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
    rawValue = rawValue.replace(/,/g, '');  // remove existing commas

    const numericValue = Number(rawValue);
    if (!isNaN(numericValue) && rawValue !== '') {
      // Format with commas, e.g. 200000 -> "200,000"
      control.setValue(numericValue.toLocaleString('en-US'), { emitEvent: false });
    }
  }

  registerSeller(formValue: any): void {
    if (this.sellerForm.invalid) return;

    // Remove commas and parse to number
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
        this.toastr.success('Vendedor creado exitosamente.', 'Éxito');
        this.sellerForm.reset();
      },
      error: (err) => {
        this.toastr.error('Error al crear el vendedor. ' + err.message, 'Error');
      }
    });
  }
}