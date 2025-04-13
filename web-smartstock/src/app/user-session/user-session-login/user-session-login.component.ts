import {
  ChangeDetectorRef,
  Component,
  OnInit,
} from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { SessionManager } from '../../services/session-manager.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserSession } from '../../dtos/user-session';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-user-session-login',
  templateUrl: './user-session-login.component.html',
  styleUrls: ['./user-session-login.component.css'],
})

export class UserSessionLoginComponent implements OnInit {

  error: string = "";

  loginForm: FormGroup;
  formSelected: String;

  constructor(
    private userSessionService: SessionManager,
    private formBuilder: FormBuilder,
    private toastrService: ToastrService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private translate: TranslateService,
  ) {
    this.loginForm = new FormGroup('');
  }

  ngOnInit() {
    this.error = '';
    this.formSelected = 'login';
    this.initial();
  }

  initial() {
    // Valida si la sesión ya está activa y, si es válida, redirige a home
    
    this.userSessionService.isSessionValid().subscribe((isValid) => {
      if (this.userSessionService.isSessionActive() && isValid) {
        this.router.navigate([`/home`]);
      }
    });
  
    this.loginForm = this.formBuilder.group({
      email: [
        'admin.admin@sta.com',
        [
          Validators.required,
          Validators.pattern('[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,4}$'),
        ],
      ],
      password: [
        '123456',
        [
          Validators.required,
          Validators.maxLength(50),
          Validators.minLength(4),
        ],
      ],
    });
  }

  loginUser(userSession: UserSession) {
    this.userSessionService.login(userSession).subscribe({
      next: (res) => {
        this.userSessionService.saveSession(res.token, res.user_id, res.type);
        this.toastrService.success(
          this.translate.instant('LOGIN.SUCCESS_MESSAGE'),
          this.translate.instant('LOGIN.SUCCESS_TITLE'),
          { closeButton: true }
        );

        // Redirige a la página de inicio después de iniciar sesión
        this.router.navigate([`/home`]);
      },
      error: (err: Error) => {
        if (err.message === 'invalid credentials') {
          this.error =  this.translate.instant('LOGIN.LOGIN_ERROR');
        }
      },
    });
  }

  redirectToSignUp() {
    this.formSelected = 'signup';
  }
}
