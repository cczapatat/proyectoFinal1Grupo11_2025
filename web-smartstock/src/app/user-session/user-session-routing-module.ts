import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserSessionSignUpComponent } from './user-session-sign-up/user-session-sign-up.component';
const routes: Routes = [{
  path: 'register',
  children: [
    {
      path: '',
      component: UserSessionSignUpComponent
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
