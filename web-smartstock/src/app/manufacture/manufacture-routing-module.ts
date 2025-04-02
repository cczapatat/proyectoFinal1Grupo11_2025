import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ManufactureListProductsComponent } from './manufacture-list-products/manufacture-list-products.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'manufacturers',
  children: [
    {
      path: 'list-products',
      component: ManufactureListProductsComponent,  canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManufactureRoutingModule { }
