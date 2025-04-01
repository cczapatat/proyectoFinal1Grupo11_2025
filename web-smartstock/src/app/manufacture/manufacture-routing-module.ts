import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ManufactureListProductsComponent } from './manufacture-list-products/manufacture-list-products.component';

const routes: Routes = [{
  path: 'manufacturers',
  children: [
    {
      path: 'list-products',
      component: ManufactureListProductsComponent
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManufactureRoutingModule { }
