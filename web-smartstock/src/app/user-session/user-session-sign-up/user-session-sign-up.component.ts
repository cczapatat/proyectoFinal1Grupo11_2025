import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { SessionManager } from '../../services/session-manager.service';
import { UserSession } from '../user-session';
import { EnumsService } from 'src/app/enums.service';
import { Banco } from 'src/app/enums';

@Component({
  selector: 'app-user-session-sign-up',
  templateUrl: './user-session-sign-up.component.html',
  styleUrls: ['./user-session-sign-up.component.css']
})
export class UserSessionSignUpComponent implements OnInit {

  userTypeList = [
    { name: 'admin' },
    { name: 'propietario' },
  ];

  @Output() newItemEvent = new EventEmitter<string>();
  @Output() newUserRegisterEvent = new EventEmitter<string>();

  finalForm: FormGroup;
  administradorForm: FormGroup;
  usuarioForm: FormGroup;
  isVisible: Number = 0;

  listaBancos: Banco[] = [];

  constructor(
    private usuarioService: SessionManager,
    private formBuilder: FormBuilder,
    private router: Router,
    private toastrService: ToastrService,
    private enumService: EnumsService,
  ) {
    this.finalForm = new FormGroup('')
    this.administradorForm = new FormGroup('')
    this.usuarioForm = new FormGroup('')
  }

  onItemChange(index) {
    this.isVisible = index;

    if (this.isVisible == 0) {
      this.finalForm = this.administradorForm
      this.newItemEvent.emit("Administrador de propiedades de corta estancia")
    } else {
      this.finalForm = this.usuarioForm
      this.newItemEvent.emit("Propietario en corta estancia")
    }
  }

  ngOnInit() {
    this.enumService.bancos().subscribe((bancos) => {
      this.listaBancos = bancos;
    })

    this.initial();
  }

  initial() {
    this.isVisible = 0;
    this.onItemChange(this.isVisible)
    this.administradorForm = this.formBuilder.group({
      usuario: ["", [Validators.required, Validators.maxLength(50)]],
      contrasena: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]],
      confirmarContrasena: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]]
    });

    this.usuarioForm = this.formBuilder.group({
      nombre: ["", [Validators.required, Validators.maxLength(50)]],
      telefono: ["", [Validators.required, Validators.maxLength(15)]],
      banco: [null, [Validators.required]],
      cuenta: ["", [Validators.required, Validators.maxLength(20)]],
      usuario: ["", [Validators.required, Validators.maxLength(50)]],
      correo: ["", [Validators.required, Validators.pattern("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$")]],
      contrasena: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]],
      confirmarContrasena: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]]
    });

    this.finalForm = this.administradorForm;
  }

  registrarUsuario(userSession: UserSession) {
    userSession.type = this.userTypeList[this.isVisible.valueOf()].name

    this.usuarioService.registro(userSession)
      .subscribe(() => {
        this.newUserRegisterEvent.emit("login")
        this.toastrService.success("Registro exitoso", this.userTypeList[this.isVisible.valueOf()].name + " registrado correctamente.")
      });
  }
}
