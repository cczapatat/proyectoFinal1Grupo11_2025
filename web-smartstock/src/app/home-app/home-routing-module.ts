import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PropiedadListaComponent } from './home/home.component';
import { AuthGuard } from '../guards/auth.guard';

const routes: Routes = [{
  path: 'home',
  children: [
    {
      path: '',
      component: PropiedadListaComponent, canActivate: [AuthGuard],
    },
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PropiedadRoutingModule { }
