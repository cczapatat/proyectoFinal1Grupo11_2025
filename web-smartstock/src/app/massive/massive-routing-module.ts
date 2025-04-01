import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MassiveManufacturesComponent } from './massive-manufactures/massive-manufactures.component';
import { MassiveProductsCreateComponent } from './massive-products-create/massive-products-create.component';
import { MassiveProductEditComponent } from './massive-product-edit/massive-product-edit.component';

const routes: Routes = [{
  path: 'massive',
  children: [
    {
      path: 'manufacture',
      component: MassiveManufacturesComponent
    },
    {
      path: 'product/create',
      component: MassiveProductsCreateComponent
    },
    {
      path: 'product/edit',
      component: MassiveProductEditComponent
    },
    {
      path: '',
      component: MassiveManufacturesComponent
    },
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MassiveRoutingModule { }
