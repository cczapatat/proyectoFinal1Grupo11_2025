import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-massive-manufactures',
  templateUrl: './massive-manufactures.component.html',
  styleUrls: ['./massive-manufactures.component.css']
})
export class MassiveManufacturesComponent implements OnInit {
  selectedFile: File | null = null;

  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
  }
}
