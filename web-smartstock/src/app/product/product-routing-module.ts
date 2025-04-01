import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProductCreateComponent } from './product-create/product-create.component';
import { ProductEditComponent } from './product-edit/product-edit.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'product',
  children: [
    {
      path: 'create',
      component: ProductCreateComponent, canActivate: [AuthGuard],
    },
    {
      path: 'edit',
      component: ProductEditComponent, canActivate: [AuthGuard],
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductRoutingModule { }
