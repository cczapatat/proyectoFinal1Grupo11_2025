import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-massive-products-create',
  templateUrl: './massive-products-create.component.html',
  styleUrls: ['./massive-products-create.component.css']
})
export class MassiveProductsCreateComponent implements OnInit {
  selectedFile: File | null = null;

  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
