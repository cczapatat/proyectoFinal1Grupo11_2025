import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { SessionManager } from '../../services/session-manager.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserSession } from '../../dtos/user-session';

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
    private cdr: ChangeDetectorRef
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
    console.log('Sesion activa: ' + this.userSessionService.esSesionActiva());
    this.userSessionService.esSesionValida().subscribe((isValid) => {
      console.log('Sesion valida: ' + isValid);
      if (this.userSessionService.esSesionActiva() && isValid) {
        this.router.navigate([`/home`]);
      }
    });
  
    this.loginForm = this.formBuilder.group({
      email: [
        '',
        [
          Validators.required,
          Validators.pattern('[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,4}$'),
        ],
      ],
      password: [
        '',
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
        this.userSessionService.guardarSesion(res.token, res.userId, res.type);
        this.toastrService.success(
          `Login successful as ${res.type}`,
          'Information',
          { closeButton: true }
        );

        // Redirige a la página de inicio después de iniciar sesión
        this.router.navigate([`/home`]);
      },
      error: (err: Error) => {
        if (err.message === 'invalid credentials') {
          this.error = 'Credentials provided are not valid';
        }
      },
    });
  }

  redirectToSignUp() {
    this.formSelected = 'signup';
  }
}
