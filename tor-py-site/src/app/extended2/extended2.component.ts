import { Component, OnInit } from '@angular/core';
import { Buffer } from "buffer"
import { Created2Data } from '../created2/created2.component';

@Component({
  selector: 'app-extended2',
  templateUrl: './extended2.component.html',
  styleUrls: ['./extended2.component.css']
})
export class Extended2Component implements OnInit {
  data: Created2Data
  ephServerPublicKey: string
  serverAuth: string

  ngOnInit() {
    this.ephServerPublicKey = Buffer.from(this.data.payload.ephServerPublicKey).toString("hex")
    this.serverAuth = Buffer.from(this.data.payload.serverAuth).toString("hex")
  }
}
