import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-salespeople-assign-customers',
  templateUrl: './salespeople-assign-customers.component.html',
  styleUrls: ['./salespeople-assign-customers.component.css']
})
export class SalespeopleAssignCustomersComponent implements OnInit {
  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
