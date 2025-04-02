import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OrderCreateComponent } from './order-create/order-create.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'order',
  children: [
    {
      path: 'create',
      component: OrderCreateComponent, canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrderRoutingModule { }
