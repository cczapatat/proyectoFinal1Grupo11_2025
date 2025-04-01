import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AlarmRoutingModule } from './alarm-routing-module';
import { AlarmCreateComponent } from './alarm-create/alarm-create.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    AlarmRoutingModule
  ],
  declarations: [
    AlarmCreateComponent,
  ],
  exports: [
    AlarmCreateComponent,
  ]
})
export class AlarmModule { }
