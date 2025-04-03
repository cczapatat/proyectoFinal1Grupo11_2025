import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { SessionManager } from 'src/app/services/session-manager.service';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  isMenuVisible = false;
  isAdmin = false;
  currentLang: string = 'es-CO';
  availableLangs = ['en-UK', 'es-AR', 'es-CO'];

  constructor(
    private router: Router,
    private toastrService: ToastrService,
    private sessionManager: SessionManager,
    private translate: TranslateService
  ) { }

  ngOnInit() {
    this.isAdmin = this._isAdmin();
    this.initializeLanguage();
  }

  toggleMenu() {
    this.isMenuVisible = !this.isMenuVisible;
  }

  hideMenu() {
    this.isMenuVisible = false;
  }

  navigate(route: string) {
    this.router.navigate([route]);
    this.hideMenu();
  }

  logOut() {
    this.sessionManager.closeSession();
    this.toastrService.success(
      this.translate.instant('NAV.LOGOUT_MESSAGE'),
      this.translate.instant('NAV.LOGOUT'),
      { closeButton: true }
    );
  }

  private _isAdmin(): boolean {
    const type = localStorage.getItem('type');
    const isAdmin = type === 'ADMIN';

    return isAdmin;
  }

  private initializeLanguage() {
    const browserLang = navigator.language;
    const matchedLang = this.availableLangs.find(lang => 
      lang.toLowerCase() === browserLang.toLowerCase()
    );
    this.currentLang = matchedLang || 'es-CO';
    this.translate.setDefaultLang('es-CO');
    this.translate.use(this.currentLang);
  }

  changeLanguage(lang: string) {
    this.currentLang = lang;
    this.translate.use(lang);
  }
}
