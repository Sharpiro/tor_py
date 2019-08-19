import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-relay-resolved',
  templateUrl: './relay-resolved.component.html',
  styleUrls: ['./relay-resolved.component.css']
})
export class RelayResolvedComponent implements OnInit {
  data: RelayResolvedData

  constructor() { }

  ngOnInit() {
  }
}

interface RelayResolvedData {
  cell: any
  ipAddress: string
}
