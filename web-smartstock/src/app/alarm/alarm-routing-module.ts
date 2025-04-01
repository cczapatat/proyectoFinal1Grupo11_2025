import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AlarmCreateComponent } from './alarm-create/alarm-create.component';

const routes: Routes = [{
  path: 'alarm',
  children: [
    {
      path: 'create',
      component: AlarmCreateComponent
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AlarmRoutingModule { }
