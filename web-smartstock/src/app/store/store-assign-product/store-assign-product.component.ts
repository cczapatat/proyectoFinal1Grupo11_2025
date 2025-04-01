import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-store-assign-product',
  templateUrl: './store-assign-product.component.html',
  styleUrls: ['./store-assign-product.component.css']
})
export class StoreAssignProductComponent implements OnInit {
  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
