import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { StoreRegisterComponent } from './store-register/store-register.component';
import { StoreAssignProductComponent } from './store-assign-product/store-assign-product.component';

const routes: Routes = [{
  path: 'store',
  children: [
    {
      path: 'register',
      component: StoreRegisterComponent
    },
    {
      path: 'assign-product',
      component: StoreAssignProductComponent
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StoreRoutingModule { }
