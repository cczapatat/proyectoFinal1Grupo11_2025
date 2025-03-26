import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';
import { ModalModule } from 'ngx-bootstrap/modal'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserSessionModule } from './user-session/user-session.module';
import { HeaderAppModule } from './header-app/header-app.module';
import { UsuarioRoutingModule } from './user-session/user-session-routing-module';
import { HttpErrorInterceptorService } from './interceptors/http-error-interceptor.service';
import { PropiedadRoutingModule } from './home-app/home-routing-module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    HeaderAppModule,
    UserSessionModule,
    UsuarioRoutingModule,
    PropiedadRoutingModule,
    ToastrModule.forRoot({
      timeOut: 7000,
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
    HttpClientModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
