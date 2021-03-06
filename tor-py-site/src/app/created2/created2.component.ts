import { Component, OnInit } from '@angular/core';
import { Buffer } from "buffer"

@Component({
  selector: 'app-created2',
  templateUrl: './created2.component.html',
  styleUrls: ['./created2.component.css']
})
export class Created2Component implements OnInit {
  data: Created2Data
  ephServerPublicKey: string
  serverAuth: string

  ngOnInit(): void {
    this.ephServerPublicKey = Buffer.from(this.data.payload.ephServerPublicKey).toString("hex")
    this.serverAuth = Buffer.from(this.data.payload.serverAuth).toString("hex")
  }
}

export interface Created2Data {
  payload: Created2Payload
}

export interface Created2Payload {
  ephServerPublicKey: number[]
  serverAuth: number[]
}
