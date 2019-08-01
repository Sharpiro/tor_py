import { Component, OnInit } from '@angular/core';
import { Buffer } from "buffer"

@Component({
  selector: 'app-create2',
  templateUrl: './create2.component.html',
  styleUrls: ['./create2.component.css']
})
export class Create2Component implements OnInit {
  data: Create2Data;
  ephMyPrivateKey: string
  ephMyPublicKey: string
  serverIdentityDigest: string
  onionKey: string

  ngOnInit(): void {
    this.ephMyPrivateKey = Buffer.from(this.data.handshakeData.ephMyPrivateKey).toString("hex")
    this.ephMyPublicKey = Buffer.from(this.data.handshakeData.ephMyPublicKey).toString("hex")
    this.serverIdentityDigest = Buffer.from(this.data.handshakeData.serverIdentityDigest).toString("hex")
    this.onionKey = Buffer.from(this.data.handshakeData.onionKey).toString("base64")
  }
}

interface Create2Data {
  handshakeData: HandshakeData
}

interface HandshakeData {
  handshakeType: number
  ephMyPrivateKey: number[]
  ephMyPublicKey: number[]
  serverIdentityDigest: number[]
  onionKey: number[]
}
