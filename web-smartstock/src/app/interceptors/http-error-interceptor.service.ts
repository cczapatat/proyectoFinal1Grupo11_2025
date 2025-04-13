import {
  HttpEvent,
  HttpHandler,
  HttpRequest,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';
import { Injectable } from '@angular/core';

@Injectable()
export class HttpErrorInterceptorService extends HttpErrorResponse {
  constructor(private toastrService: ToastrService) { super(toastrService) }
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request)
      .pipe(
        catchError((httpErrorResponse: HttpErrorResponse) => {
          let errorMessage = '';

          if (httpErrorResponse.error instanceof ErrorEvent) {
            errorMessage = httpErrorResponse.error.error;
          } else {
            if (httpErrorResponse.status === 0) {
              errorMessage = "Do not have server connection";
            } else {
              if (httpErrorResponse.error.statusText === "UNAUTHORIZED") {
                errorMessage = 'Su sesión ha caducado, por favor vuelva a iniciar sesión.';
              }
              else if (httpErrorResponse.error.statusText === "UNPROCESSABLE ENTITY") {
                errorMessage = 'No hemos podido identificarlo, por favor vuelva a iniciar sesión.';
              }
              else {
                const error = typeof httpErrorResponse.error === 'string'
                  ? httpErrorResponse.error
                  : httpErrorResponse.error.message;
                errorMessage = `Ha ocurrido un error. ${error}`;
              }
            }
          }
          this.toastrService.error(errorMessage, 'Error', { progressBar: true, closeButton: true });
          return throwError(() => new Error(errorMessage));
        })
      )
  }
}