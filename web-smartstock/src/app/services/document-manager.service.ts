import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment'
import { Document } from '../massive/document';

@Injectable({
  providedIn: 'root'
})
export class DocumentManagerService {

  private apiDocumentManagerUrl = environment.apiDocumentManagerUrl;

  constructor(
    private http: HttpClient
  ) { }

  uploadFile(file: File): Observable<Document> {
    const headers = new HttpHeaders({
      'x-token': 'internal_token',
      'user-id': '11189d7f-f3a2-44d9-82f5-b339d97bcdd5'
    });
  
    const formData = new FormData();
    formData.append('file', file);
  
    return this.http.post<Document>(`${this.apiDocumentManagerUrl}/document/create`, formData, { headers });
  }
}

