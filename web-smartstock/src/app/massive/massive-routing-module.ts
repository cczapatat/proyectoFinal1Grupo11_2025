import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MassiveManufacturesComponent } from './massive-manufactures/massive-manufactures.component';
import { MassiveProductsCreateComponent } from './massive-products-create/massive-products-create.component';
import { MassiveProductEditComponent } from './massive-product-edit/massive-product-edit.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'massive',
  children: [
    {
      path: 'manufacture',
      component: MassiveManufacturesComponent , canActivate: [AuthGuard],
    },
    {
      path: 'product/create',
      component: MassiveProductsCreateComponent, canActivate: [AuthGuard],
    },
    {
      path: 'product/edit',
      component: MassiveProductEditComponent, canActivate: [AuthGuard],
    },
    {
      path: '',
      component: MassiveManufacturesComponent, canActivate: [AuthGuard],
    },
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MassiveRoutingModule { }
