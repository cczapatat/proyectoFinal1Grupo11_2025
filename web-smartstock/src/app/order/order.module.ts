import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { OrderRoutingModule } from './order-routing-module';
import { OrderCreateComponent } from './order-create/order-create.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    OrderRoutingModule,
    FormsModule,
    TranslateModule,
  ],
  declarations: [
    OrderCreateComponent,
  ],
  exports: [
    OrderCreateComponent,
  ]
})
export class OrderModule { }
