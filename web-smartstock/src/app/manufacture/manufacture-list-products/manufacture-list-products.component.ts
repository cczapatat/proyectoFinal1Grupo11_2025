import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-manufacture-list-products',
  templateUrl: './manufacture-list-products.component.html',
  styleUrls: ['./manufacture-list-products.component.css']
})
export class ManufactureListProductsComponent implements OnInit {
  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
