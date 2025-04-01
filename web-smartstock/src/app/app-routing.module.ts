import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserSessionLoginComponent } from './user-session/user-session-login/user-session-login.component';
import { HomeComponent } from './home-app/home/home.component';

const routes: Routes = [
  { path: '', redirectTo: '/user-sessions/login', pathMatch: 'full' },
  { path: 'user-sessions/login', component: UserSessionLoginComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
