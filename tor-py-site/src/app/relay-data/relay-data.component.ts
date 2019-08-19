import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-relay-data',
  templateUrl: './relay-data.component.html',
  styleUrls: ['./relay-data.component.css']
})
export class RelayDataComponent implements OnInit {
  data: RelayDataData

  constructor() { }

  ngOnInit() {
  }
}

interface RelayDataData {
  cell: any
  payload: string
}
