import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-massive-product-edit',
  templateUrl: './massive-product-edit.component.html',
  styleUrls: ['./massive-product-edit.component.css']
})
export class MassiveProductEditComponent implements OnInit {
  selectedFile: File | null = null;

  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
