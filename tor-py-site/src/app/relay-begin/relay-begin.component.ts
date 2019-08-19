import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-relay-begin',
  templateUrl: './relay-begin.component.html',
  styleUrls: ['./relay-begin.component.css']
})
export class RelayBeginComponent implements OnInit {
  data: RelayBeginData

  constructor() { }

  ngOnInit() {
  }
}

interface RelayBeginData {
  cell: any
  addrPort: string
}
