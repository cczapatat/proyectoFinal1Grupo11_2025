import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProductCreateComponent } from './product-create/product-create.component';
import { ProductEditComponent } from './product-edit/product-edit.component';
import { AuthGuard } from '../guards/auth.guard';
import { ProductListComponent } from './product-list/product-list.component';

const routes: Routes = [{
  path: 'product',
  children: [
    {
      path: 'create',
      component: ProductCreateComponent, canActivate: [AuthGuard],
    },
    {
      path: 'list',
      component: ProductListComponent, canActivate: [AuthGuard],
    },
    {
      path: 'edit/:id',
      component: ProductEditComponent, canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductRoutingModule { }
