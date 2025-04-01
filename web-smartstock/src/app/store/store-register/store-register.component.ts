import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-store-register',
  templateUrl: './store-register.component.html',
  styleUrls: ['./store-register.component.css']
})
export class StoreRegisterComponent implements OnInit {
  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
