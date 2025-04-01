import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { SessionManager } from 'src/app/services/session-manager.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(
    private toastrService: ToastrService,
    private sessionManager: SessionManager
  ) { }

  ngOnInit() {
  }

  logOut() {
    this.sessionManager.cerrarSesion();
    this.toastrService.success(
      `Log Out successfully`
      , "Information", 
      { closeButton: true }
    );
  }

}
