/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { faker } from '@faker-js/faker';

import { MassiveProductEditComponent } from './massive-product-edit.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ToastrModule } from 'ngx-toastr';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { DocumentManagerService } from '../../services/document-manager.service';
import { of } from 'rxjs';

import { Document } from '../document';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { BulkTask } from 'src/app/dtos/bulk-task';

describe('MassiveProductsEditComponent', () => {
  let component: MassiveProductEditComponent;
  let fixture: ComponentFixture<MassiveProductEditComponent>;
  let debug: DebugElement;

  let documentManagerService: jasmine.SpyObj<DocumentManagerService>;
  let productService: jasmine.SpyObj<ProductService>;

  beforeEach(async(() => {
    const documentManagerServiceSpy = jasmine.createSpyObj('DocumentManagerService', ['uploadFile']);
    const productServiceSpy = jasmine.createSpyObj('ProductService', ['updateMassiveProducts']);

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
        { provide: ProductService, useValue: productServiceSpy },
        FormBuilder,
        TranslateService
      ],
      declarations: [ MassiveProductEditComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MassiveProductEditComponent);
    component = fixture.componentInstance;
    debug = fixture.debugElement;

    documentManagerService = TestBed.inject(DocumentManagerService) as jasmine.SpyObj<DocumentManagerService>;
    productService = TestBed.inject(ProductService) as jasmine.SpyObj<ProductService>;
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
    productService.updateMassiveProducts.and.returnValue(of(
      new BulkTask(
        faker.date.past(),
        faker.string.uuid().toString(),
        faker.string.uuid().toString(),
        'QUEUE',
        faker.date.past()
      )
    ));

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
});
