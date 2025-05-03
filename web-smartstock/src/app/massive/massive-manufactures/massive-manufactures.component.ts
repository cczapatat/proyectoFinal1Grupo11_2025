import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { DocumentManagerService } from 'src/app/services/document-manager.service';
import { ManufacturerService } from 'src/app/services/manufacturer.service';

@Component({
  selector: 'app-massive-manufactures',
  templateUrl: './massive-manufactures.component.html',
  styleUrls: ['./massive-manufactures.component.css']
})
export class MassiveManufacturesComponent implements OnInit {
  selectedFile: File | null = null;
  selectedFileSize: string | null = null;
  fileRequiredError = false;
  fileSizeError: string | null = null;
  fileUploaded = false;
  readonly MAX_FILE_SIZE_MB = 300;

  constructor(
    private routerPath: Router,
    private documentManagerService: DocumentManagerService,
    private manufacturerService: ManufacturerService,
    private toastr: ToastrService,
    private translate: TranslateService,
  ) {}

  ngOnInit(): void {
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
  
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
  
      const maxSizeBytes = this.MAX_FILE_SIZE_MB * 1024 * 1024;
      if (file.size > maxSizeBytes) {
        this.fileSizeError = `El archivo supera el tamaño máximo permitido de ${this.MAX_FILE_SIZE_MB} MB.`;
        this.selectedFile = null;
        this.selectedFileSize = null;
        return;
      }
  
      this.fileSizeError = null;
      this.selectedFile = file;
  
      if (file.size < 1024) {
        this.selectedFileSize = `${file.size} bytes`;
      } else if (file.size < 1024 * 1024) {
        this.selectedFileSize = `${(file.size / 1024).toFixed(2)} KB`;
      } else {
        this.selectedFileSize = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
      }
    }
  }

  createMassiveManufacturer(): void {
    if (!this.selectedFile) {
      this.fileRequiredError = true;
      return;
    }

    this.documentManagerService.uploadFile(this.selectedFile).subscribe(
      (response) => {
        this.manufacturerService.createMassiveManufacturers(response.id).subscribe(
          (response) => {
            this.fileUploaded = true;
            this.fileRequiredError = false;
            this.toastr.success(this.translate.instant('MASSIVES.UPLOAD_FILE_SUCCESS_TITLE'), this.translate.instant('MASSIVES.UPLOAD_FILE_SUCCESS_DESCRIPTION'));
            
          },
          (error) => {
            this.toastr.error(this.translate.instant('MASSIVES.UPLOAD_FILE_ERROR_TITLE'), this.translate.instant('MASSIVES.UPLOAD_FILE_ERROR_DESCRIPTION'));
            console.error('Error creating massive products:', error); 
            this.fileRequiredError = true;
            this.selectedFile = null;
          }
        );
      },
      (error) => {
        this.toastr.error(this.translate.instant('MASSIVES.UPLOAD_FILE_ERROR_TITLE'), this.translate.instant('MASSIVES.UPLOAD_FILE_ERROR_DESCRIPTION'));
        console.error('Error uploading file:', error); 
        this.fileRequiredError = true;
        this.selectedFile = null;
      }
    );
  }
}
