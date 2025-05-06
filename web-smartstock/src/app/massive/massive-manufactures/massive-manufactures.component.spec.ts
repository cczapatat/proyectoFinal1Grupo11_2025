/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { faker } from '@faker-js/faker';

import { MassiveManufacturesComponent } from './massive-manufactures.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ActiveToast, ToastrModule, ToastrService } from 'ngx-toastr';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ManufacturerService } from '../../services/manufacturer.service';
import { DocumentManagerService } from '../../services/document-manager.service';
import { of, throwError } from 'rxjs';

import { Document } from '../document';
import { TranslateModule, TranslatePipe, TranslateService } from '@ngx-translate/core';
import { BulkTask } from 'src/app/dtos/bulk-task';

describe('MassiveProductsCreateComponent', () => {
  let component: MassiveManufacturesComponent;
  let fixture: ComponentFixture<MassiveManufacturesComponent>;
  let debug: DebugElement;

  let documentManagerService: jasmine.SpyObj<DocumentManagerService>;
  let manufacturerService: jasmine.SpyObj<ManufacturerService>;
  let toastr: jasmine.SpyObj<ToastrService>;

  beforeEach(async(() => {
    const documentManagerServiceSpy = jasmine.createSpyObj('DocumentManagerService', ['uploadFile']);
    const manufacturerServiceSpy = jasmine.createSpyObj('ManufacturerService', ['createMassiveManufacturers']);
    const toastrSpy = jasmine.createSpyObj('ToastrService', ['success', 'error']);

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
        ToastrModule.forRoot(),
        TranslateModule.forRoot(),
        ReactiveFormsModule
      ],
      providers: [
        { provide: DocumentManagerService, useValue: documentManagerServiceSpy },
        { provide: ManufacturerService, useValue: manufacturerServiceSpy },
        { provide: ToastrService, useValue: toastrSpy },
        FormBuilder,
        TranslateService
      ],
      declarations: [ MassiveManufacturesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MassiveManufacturesComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    documentManagerService = TestBed.inject(DocumentManagerService) as jasmine.SpyObj<DocumentManagerService>;
    manufacturerService = TestBed.inject(ManufacturerService) as jasmine.SpyObj<ManufacturerService>;
    toastr = TestBed.inject(ToastrService) as jasmine.SpyObj<ToastrService>;
  }));

  beforeEach(() => {
    documentManagerService.uploadFile.and.returnValue(of(
      new Document(
        faker.string.uuid(),
        faker.system.fileName(),
        faker.system.filePath(),
        faker.string.uuid(),
        faker.date.past().toString(),
        faker.date.past().toString()
      )
    ));
    manufacturerService.createMassiveManufacturers.and.returnValue(of(
      new BulkTask(
        faker.date.past(),
        faker.string.uuid().toString(),
        faker.string.uuid().toString(),
        'QUEUE',
        faker.date.past()
      )
    ));

    const mockActiveToast = {} as ActiveToast<any>;

  toastr.success.and.callFake((title: string, description: string) => {
    console.log(`Success: ${title} - ${description}`);
    return mockActiveToast; // Return a mock ActiveToast object
  });

  toastr.error.and.callFake((title: string, description: string) => {
    console.log(`Error: ${title} - ${description}`);
    return mockActiveToast; // Return a mock ActiveToast object
  });

  fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("Component has a title", () => {
    let title = debug.query(By.css('h1')).nativeElement;
    expect(title.innerHTML).toBeTruthy();
  });

  it("Component has an upload icon", () => {
    expect(debug.queryAll(By.css('#upload-icon'))).toHaveSize(1);
  });

  it("Component has an uploaded icon", () => {
    component.selectedFile = new File([], 'test.txt');
    component.selectedFileSize = '1 MB';
    component.fileUploaded = true;
    fixture.detectChanges();
    expect(debug.queryAll(By.css('#uploaded-icon'))).toHaveSize(1);
  });

  it("Component has an upload description", () => {
    component.selectedFile = null;
    component.fileUploaded = false;
    fixture.detectChanges();
    expect(debug.queryAll(By.css('#upload_description'))).toHaveSize(1);
  });

  it("Component has an file_info description", () => {
    component.selectedFile = new File([], 'test.txt');
    component.selectedFileSize = '1 MB';
    component.fileUploaded = false;
    fixture.detectChanges();
    expect(debug.queryAll(By.css('#file_info'))).toHaveSize(1);
  });

  it("Component has an uploaded description", () => {
    component.selectedFile = new File([], 'test.txt');
    component.selectedFileSize = '1 MB';
    component.fileUploaded = true;
    fixture.detectChanges();

    expect(debug.queryAll(By.css('#uploaded_description'))).toHaveSize(1);
  });

  it("Component has an input file", () => {
    expect(debug.queryAll(By.css('#file_input'))).toHaveSize(1);
  });

  it("Component has an upload button", () => {
    expect(debug.queryAll(By.css('#upload_btn'))).toHaveSize(1);
  });

  it("Component has an proccess button", () => {
    expect(debug.queryAll(By.css('#upload_btn'))).toHaveSize(1);
  });

  it("Component has an file_restrictions description", () => {
    expect(debug.queryAll(By.css('#file_restrictions'))).toHaveSize(1);
  });

  it("Component has an file_uploaded_notification description", () => {
    component.selectedFile = new File([], 'test.txt');
    component.selectedFileSize = '1 MB';
    component.fileUploaded = true;
    fixture.detectChanges();
    expect(debug.queryAll(By.css('#file_uploaded_notification'))).toHaveSize(1);
  });

  it("Component has an file_size_error description", () => {
    component.fileSizeError = 'El archivo supera el tamaño máximo permitido de 300 MB.';
    fixture.detectChanges();
    expect(debug.queryAll(By.css('#file_size_error'))).toHaveSize(1);
  });

  it('should set selectedFile and selectedFileSize when a valid file is selected', () => {
    const fileContent = 'a'.repeat(1024 * 1024);
    const file = new File([fileContent], 'test-file.csv', { type: 'text/csv' });
    const event = { target: { files: [file] } } as unknown as Event;
  
    component.onFileSelected(event);
  
    expect(component.selectedFile).toBe(file);
    expect(component.selectedFileSize).toBe('1.00 MB');
    expect(component.fileSizeError).toBeNull();
  });

  it('should set selectedFile and selectedFileSize in bytes when a valid file is selected', () => {
    const fileContent = 'a'.repeat(10);
    const file = new File([fileContent], 'test-file.csv', { type: 'text/csv' });
    const event = { target: { files: [file] } } as unknown as Event;
  
    component.onFileSelected(event);
  
    expect(component.selectedFile).toBe(file);
    expect(component.selectedFileSize).toBe('10 bytes');
    expect(component.fileSizeError).toBeNull();
  });

  it('should set selectedFile and selectedFileSize in bytes when a valid file is selected', () => {
    const fileContent = 'a'.repeat(10 * 1024);
    const file = new File([fileContent], 'test-file.csv', { type: 'text/csv' });
    const event = { target: { files: [file] } } as unknown as Event;
  
    component.onFileSelected(event);
  
    expect(component.selectedFile).toBe(file);
    expect(component.selectedFileSize).toBe('10.00 KB');
    expect(component.fileSizeError).toBeNull();
  });
  
  it('should set fileSizeError when the file exceeds the maximum size', () => {
    const fileContent = 'a'.repeat(301 * 1024 * 1024);
    const file = new File([fileContent], 'large-file.csv', { type: 'text/csv' });
    const event = { target: { files: [file] } } as unknown as Event;
  
    component.onFileSelected(event);
  
    expect(component.selectedFile).toBeNull();
    expect(component.selectedFileSize).toBeNull();
    expect(component.fileSizeError).toBe(`El archivo supera el tamaño máximo permitido de ${component.MAX_FILE_SIZE_MB} MB.`);
  });

  it('should do nothing when no file is selected', () => {
    const event = { target: { files: [] } } as unknown as Event;

    component.onFileSelected(event);

    expect(component.selectedFile).toBeNull();
    expect(component.selectedFileSize).toBeNull();
    expect(component.fileSizeError).toBeNull();
  });

  it('should set fileRequiredError to true if no file is selected', () => {
    component.selectedFile = null;

    component.createMassiveManufacturer();

    expect(component.fileRequiredError).toBeTrue();
    expect(documentManagerService.uploadFile).not.toHaveBeenCalled();
    expect(manufacturerService.createMassiveManufacturers).not.toHaveBeenCalled();
  });

  it('should upload the file and create manufacturers successfully', () => {
    const mockFile = new File(['dummy content'], 'test.csv', { type: 'text/csv' });
    const mockDocument = new Document(
      faker.string.uuid(),
      faker.system.fileName(),
      faker.system.filePath(),
      faker.string.uuid(),
      faker.date.past().toString(),
      faker.date.past().toString()
    );
    const mockBulkTask = new BulkTask(
      faker.date.past(),
      faker.string.uuid().toString(),
      faker.string.uuid().toString(),
      'QUEUE',
      faker.date.past(),
    );

    component.selectedFile = mockFile;
    documentManagerService.uploadFile.and.returnValue(of(mockDocument));
    manufacturerService.createMassiveManufacturers.and.returnValue(of(mockBulkTask));

    component.createMassiveManufacturer();

    expect(documentManagerService.uploadFile).toHaveBeenCalledWith(mockFile);
    expect(manufacturerService.createMassiveManufacturers).toHaveBeenCalledWith(mockDocument.id);
    expect(component.fileUploaded).toBeTrue();
    expect(component.fileRequiredError).toBeFalse();
    expect(toastr.success).toHaveBeenCalled();
  });

  it('should handle file upload failure', () => {
    const mockFile = new File(['dummy content'], 'test.csv', { type: 'text/csv' });

    component.selectedFile = mockFile;
    documentManagerService.uploadFile.and.returnValue(throwError(() => new Error('Upload failed')));

    component.createMassiveManufacturer();

    expect(documentManagerService.uploadFile).toHaveBeenCalledWith(mockFile);
    expect(manufacturerService.createMassiveManufacturers).not.toHaveBeenCalled();
    expect(component.fileRequiredError).toBeTrue();
    expect(component.selectedFile).toBeNull();
    expect(toastr.error).toHaveBeenCalled();
  });

  it('should handle manufacturer creation failure', () => {
    const mockFile = new File(['dummy content'], 'test.csv', { type: 'text/csv' });
    const mockDocument = new Document(
      faker.string.uuid(),
      faker.system.fileName(),
      faker.system.filePath(),
      faker.string.uuid(),
      faker.date.past().toString(),
      faker.date.past().toString()
    );;

    component.selectedFile = mockFile;
    documentManagerService.uploadFile.and.returnValue(of(mockDocument));
    manufacturerService.createMassiveManufacturers.and.returnValue(throwError(() => new Error('Creation failed') ));

    component.createMassiveManufacturer();

    expect(documentManagerService.uploadFile).toHaveBeenCalledWith(mockFile);
    expect(manufacturerService.createMassiveManufacturers).toHaveBeenCalledWith(mockDocument.id);
    expect(component.fileRequiredError).toBeTrue();
    expect(component.selectedFile).toBeNull();
    expect(toastr.error).toHaveBeenCalled();
  });
});
