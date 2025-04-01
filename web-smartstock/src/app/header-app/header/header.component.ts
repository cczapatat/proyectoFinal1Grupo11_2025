import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { SessionManager } from 'src/app/services/session-manager.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  isMenuVisible = false;
  isAdmin = false;

  constructor(
    private router: Router,
    private toastrService: ToastrService,
    private sessionManager: SessionManager
  ) { }

  ngOnInit() {
    this.isAdmin = this._isAdmin();
  }

  toggleMenu() {
    this.isMenuVisible = !this.isMenuVisible;
  }

  hideMenu() {
    this.isMenuVisible = false;
  }

  logOut() {
    this.sessionManager.cerrarSesion();
    this.toastrService.success(
      `Log Out successfully`
      , "Information", 
      { closeButton: true }
    );
  }

  private _isAdmin(): boolean {
    const type = localStorage.getItem('type');
    const isAdmin = type === 'ADMIN';

    return isAdmin;
  }
}
