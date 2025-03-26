import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserSesionLoginComponent } from './user-session/user-session-login/user-session-login.component';
import { PropiedadListaComponent } from './home-app/home/home.component';

const routes: Routes = [
  { path: '', redirectTo: '/user-sessions/login', pathMatch: 'full' },
  { path: 'user-sessions/login', component: UserSesionLoginComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
