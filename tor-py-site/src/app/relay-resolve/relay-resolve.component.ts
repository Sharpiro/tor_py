import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-relay-resolve',
  templateUrl: './relay-resolve.component.html',
  styleUrls: ['./relay-resolve.component.css']
})
export class RelayResolveComponent implements OnInit {
  data: RelayResolveData

  constructor() { }

  ngOnInit() {
  }
}

export interface RelayResolveData {
  cell: any
  hostname: string
}
