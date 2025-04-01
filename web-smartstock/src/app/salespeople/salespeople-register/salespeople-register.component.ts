import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-salespeople-register',
  templateUrl: './salespeople-register.component.html',
  styleUrls: ['./salespeople-register.component.css']
})
export class SalespeopleRegisterComponent implements OnInit {
  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
