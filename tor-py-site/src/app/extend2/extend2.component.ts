import { Component, OnInit } from '@angular/core';
import { Create2Data } from '../create2/create2.component';
import { Buffer } from "buffer"

@Component({
  selector: 'app-extend2',
  templateUrl: './extend2.component.html',
  styleUrls: ['./extend2.component.css']
})
export class Extend2Component implements OnInit {
  data: Create2Data;
  ephMyPrivateKey: string
  ephMyPublicKey: string
  serverIdentityDigest: string
  onionKey: string

  ngOnInit() {
    this.ephMyPrivateKey = Buffer.from(this.data.handshakeData.ephMyPrivateKey).toString("hex")
    this.ephMyPublicKey = Buffer.from(this.data.handshakeData.ephMyPublicKey).toString("hex")
    this.serverIdentityDigest = Buffer.from(this.data.handshakeData.serverIdentityDigest).toString("hex")
    this.onionKey = Buffer.from(this.data.handshakeData.onionKey).toString("base64")
  }
}
