import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AlarmRoutingModule } from './alarm-routing-module';
import { AlarmCreateComponent } from './alarm-create/alarm-create.component';
import { ReactiveFormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TranslateModule,
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
