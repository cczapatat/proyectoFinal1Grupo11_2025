import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { PropiedadListaComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { PropiedadRoutingModule } from './home-routing-module';


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    PropiedadRoutingModule,
  ],
  declarations: [
    PropiedadListaComponent,
  ],
  exports: [
    PropiedadListaComponent,
  ]
})
export class HomeModule { }
