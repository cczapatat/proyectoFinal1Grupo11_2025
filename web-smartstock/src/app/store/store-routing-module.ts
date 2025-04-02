import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { StoreRegisterComponent } from './store-register/store-register.component';
import { StoreAssignProductComponent } from './store-assign-product/store-assign-product.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'store',
  children: [
    {
      path: 'register',
      component: StoreRegisterComponent, canActivate: [AuthGuard],
    },
    {
      path: 'assign-product',
      component: StoreAssignProductComponent, canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StoreRoutingModule { }
