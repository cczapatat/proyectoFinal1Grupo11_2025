import { ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { JwtHelperService } from "@auth0/angular-jwt";
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserSessionService } from '../user-session.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserSession } from '../user-session';

@Component({
  selector: 'app-user-session-login',
  templateUrl: './user-session-login.component.html',
  styleUrls: ['./user-session-login.component.css']
})

export class UserSessionLoginComponent implements OnInit {

  error: string = "";
  helper = new JwtHelperService();
  loginForm: FormGroup;
  formSelected: String;

  constructor(
    private userSessionService: UserSessionService,
    private formBuilder: FormBuilder,
    private toastrService: ToastrService,
    private router: Router,
    private cdr:ChangeDetectorRef) {
      this.loginForm = new FormGroup('')
     }

  ngOnInit() {
    this.formSelected = 'login'
    localStorage.setItem('decodedToken', '');
    localStorage.setItem('token', '');
    localStorage.setItem('userId', '');
    localStorage.setItem('type', 'SELLER');

    this.initial();
  }

  initial() {
    this.loginForm = this.formBuilder.group({
      email: ["", [Validators.required, Validators.pattern("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$")]],
      password: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]],
    });
  }

  loginUser(userSession: UserSession) {
    this.error = ""

    this.userSessionService.login(userSession)
      .subscribe({
        next: res => {
          localStorage.setItem('decodedToken', this.helper.decodeToken(res.token));
          localStorage.setItem('token', res.token);
          localStorage.setItem('userId', res.id);
          localStorage.setItem('type', res.type);
          this.toastrService.success(
            `Login successful as ${res.type}`
            , "Information", 
            { closeButton: true }
          );
          
          //TODO
          this.router.navigate([`/home`])
        },
        error: () => {
          this.error = "Incorrect email or password";
        },
      })
  }

  redirectToSignUp(){
    this.formSelected = 'signup'
  }
}
