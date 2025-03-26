import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PropiedadListaComponent } from './home/home.component';

const routes: Routes = [{
  path: 'home',
  children: [
    {
      path: '',
      component: PropiedadListaComponent
    },
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PropiedadRoutingModule { }
