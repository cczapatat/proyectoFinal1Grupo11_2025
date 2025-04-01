import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'SmartStock';
  loggedIn = false;

  constructor (private router: Router) {
    this.loggedIn = this.isLoggedIn();

    this.router.events.subscribe(() => {
      this.loggedIn = this.isLoggedIn();
    })
  }

  private isLoggedIn(): boolean {
    const token = localStorage.getItem('token');
    const isLoggedIn = !!token;

    return isLoggedIn;
  }
}
