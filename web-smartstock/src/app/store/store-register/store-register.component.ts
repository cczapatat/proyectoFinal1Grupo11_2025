import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { forkJoin } from 'rxjs';

import { StoreService } from 'src/app/services/store.service';
import { StoreDto } from 'src/app/dtos/store.dto';

@Component({
  selector: 'app-store-register',
  templateUrl: './store-register.component.html',
  styleUrls: ['./store-register.component.css']
})
export class StoreRegisterComponent implements OnInit {
  public states: string[] = [];
  public securityLevels: string[] = [];

  public storeForm: FormGroup;

  constructor(
    private toastr: ToastrService,
    private fb: FormBuilder,
    private translate: TranslateService,
    private storeService: StoreService,
  ) { }

  ngOnInit(): void {
    this.getEnums();
    this.initializeForm();
  }

  get formControls() {
    return this.storeForm.controls;
  }

  getEnums(): void {
    forkJoin({
      states: this.storeService.getStates(),
      securityLevels: this.storeService.getSecurityLevels()
    }).subscribe({
      next: (response) => {
        this.states = response.states;
        this.securityLevels = response.securityLevels;
      },
      error: (error) => {
        this.toastr.success(
          this.translate.instant('STORE.REGISTER_ENUMS_ERROR_MESSAGE'),
          this.translate.instant('STORE.REGISTER_ENUMS_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    });
  }

  initializeForm(): void {
    this.storeForm = this.fb.group({
      name: ['', Validators.required],
      phone: ['', [Validators.required, Validators.pattern(/\d{11,15}$/)]],
      email: ['', [Validators.required, Validators.email]],
      address: ['', Validators.required],
      capacity: ['', [Validators.required, Validators.min(1)]],
      state: ['', Validators.required],
      securityLevel: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.storeForm.invalid) {
      return;
    }

    const storeData: StoreDto = new StoreDto(
      this.storeForm.value.name,
      this.storeForm.value.phone,
      this.storeForm.value.email,
      this.storeForm.value.address,
      this.storeForm.value.capacity,
      this.storeForm.value.state,
      this.storeForm.value.securityLevel,
    );

    this.storeService.registerStore(storeData).subscribe({
      next: (response) => {
        this.toastr.success(
          this.translate.instant('STORE.REGISTER_SUCCESS_MESSAGE'),
          this.translate.instant('STORE.REGISTER_SUCCESS_TITLE'),
          { closeButton: true },
        );
        this.storeForm.reset();
      },
      error: (error) => {
        this.toastr.success(
          this.translate.instant('STORE.REGISTER_ERROR_MESSAGE'),
          this.translate.instant('STORE.REGISTER_ERROR_TITLE'),
          { closeButton: true },
        );
      }
    })
  }
}
