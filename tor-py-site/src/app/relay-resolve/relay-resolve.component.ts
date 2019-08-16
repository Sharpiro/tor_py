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
    console.log(this.data)
  }
}

export interface RelayResolveData {
  payload: RelayResolvePayload
}

export interface RelayResolvePayload {
  hostname: string
}