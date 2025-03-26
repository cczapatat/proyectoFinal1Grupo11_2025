import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(
    private toastrService: ToastrService,
  ) { }

  ngOnInit() {
  }

  logOut() {
    this.toastrService.success(
      `Log Out successfully`
      , "Information", 
      { closeButton: true }
    );
  }

}
