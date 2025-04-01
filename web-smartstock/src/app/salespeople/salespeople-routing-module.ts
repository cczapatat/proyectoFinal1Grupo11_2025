import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SalespeopleAssignCustomersComponent } from './salespeople-assign-customers/salespeople-assign-customers.component';
import { SalespeopleRegisterComponent } from './salespeople-register/salespeople-register.component';
import { SalespeopleListCustomersComponent } from './salespeople-list-customers/salespeople-list-customers.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'salespeople',
  children: [
    {
      path: 'assign-customers',
      component: SalespeopleAssignCustomersComponent, canActivate: [AuthGuard],
    },
    {
      path: 'register',
      component: SalespeopleRegisterComponent, canActivate: [AuthGuard],
    },
    {
      path: 'list-customers',
      component: SalespeopleListCustomersComponent, canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SalespeopleRoutingModule { }
