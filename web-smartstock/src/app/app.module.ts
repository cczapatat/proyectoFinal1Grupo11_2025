import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';
import { ModalModule } from 'ngx-bootstrap/modal'

import { AppComponent } from './app.component';
import { HeaderAppModule } from './header-app/header-app.module';
import { UserSessionModule } from './user-session/user-session.module';
import { MassiveModule } from './massive/massive.module';
import { SalespeopleModule } from './salespeople/salespeople.module';
import { ProductModule } from './product/product.module';
import { StoreModule } from './store/store.module';
import { OrderModule } from './order/order.module';
import { ManufactureModule } from './manufacture/manufacture.module';
import { AlarmModule } from './alarm/alarm.module';

import { AppRoutingModule } from './app-routing.module';
import { HomeRoutingModule } from './home-app/home-routing-module';
import { UserRoutingModule } from './user-session/user-session-routing-module';
import { MassiveRoutingModule } from './massive/massive-routing-module';
import { SalespeopleRoutingModule } from './salespeople/salespeople-routing-module';
import { ProductRoutingModule } from './product/product-routing-module';
import { StoreRoutingModule } from './store/store-routing-module';
import { OrderRoutingModule } from './order/order-routing-module';
import { ManufactureRoutingModule } from './manufacture/manufacture-routing-module';
import { AlarmRoutingModule } from './alarm/alarm-routing-module';

import { HttpErrorInterceptorService } from './interceptors/http-error-interceptor.service';

import { SessionInterceptorService } from './interceptors/session-interceptor.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    HeaderAppModule,
    UserSessionModule,
    MassiveModule,
    SalespeopleModule,
    ProductModule,
    StoreModule,
    OrderModule,
    ManufactureModule,
    AlarmModule,

    AppRoutingModule,
    HomeRoutingModule,
    UserRoutingModule,
    MassiveRoutingModule,
    SalespeopleRoutingModule,
    ProductRoutingModule,
    StoreRoutingModule,
    OrderRoutingModule,
    ManufactureRoutingModule,
    AlarmRoutingModule,

    ProductModule,
    ProductRoutingModule,
    ToastrModule.forRoot({
      timeOut: 3000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
    }),
    BrowserAnimationsModule,
    ModalModule.forRoot(),
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpErrorInterceptorService,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: SessionInterceptorService,
      multi: true,
    },
    HttpClientModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
