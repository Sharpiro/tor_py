import { Injectable } from '@angular/core';
import { Subject, Observable, of, interval } from 'rxjs';
import { delay, bufferTime, concatMap, throttle } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class SocketService {
  webSocket: WebSocket
  subject: Subject<string>

  constructor() {
    this.webSocket = new WebSocket("ws://127.0.0.1:5678")
    this.subject = new Subject()
    this.webSocket.onmessage = (event) => {
      this.subject.next(event.data)
    };

    // setTimeout(() => {
    //   this.webSocket.send(JSON.stringify({
    //     title: "handshake",
    //     data: ""
    //   }))
    // }, 1000);
  }

  getMessages(): Observable<string> {
    const temp = this.subject.pipe(
      concatMap(x => of(x).pipe(delay(500)))
    )
    return temp
  }

  sendMessage() {
    const message = {
      title: "test",
      data: "the data"
    }
    this.webSocket.send(JSON.stringify(message))
  }
}
