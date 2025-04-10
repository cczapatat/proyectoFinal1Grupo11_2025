import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-salespeople-list-customers',
  templateUrl: './salespeople-list-customers.component.html',
  styleUrls: ['./salespeople-list-customers.component.css']
})
export class SalespeopleListCustomersComponent implements OnInit {
  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
