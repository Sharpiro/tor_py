import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-relay-connected',
  templateUrl: './relay-connected.component.html',
  styleUrls: ['./relay-connected.component.css']
})
export class RelayConnectedComponent implements OnInit {
  data: RelayConnectedData

  constructor() { }

  ngOnInit() {
  }
}

interface RelayConnectedData {
  cell: any
  payload: RelayConnectedPayload
}

interface RelayConnectedPayload {
  ipAddress: string
  ttl: number
}
