import { Injectable, Inject, InjectionToken } from '@angular/core';
import { Subject, Observable, of, ReplaySubject } from 'rxjs';
import { delay, concatMap } from 'rxjs/operators';
import { environment } from "../../environments/environment"

export const SOCKET_URL = new InjectionToken<string>('SocketUrl');

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  private webSocketSubject: ReplaySubject<WebSocket>
  private messageSubject = new Subject<string>()

  constructor(@Inject(SOCKET_URL) private hostAndPort: string) { }

  private get webSocket(): Observable<WebSocket> {
    if (this.webSocketSubject) return this.webSocketSubject

    this.webSocketSubject = new ReplaySubject<WebSocket>()
    const protocol = environment.production ? "wss" : "ws"
    const webSocket = new WebSocket(`${protocol}://${this.hostAndPort}`)
    webSocket.onopen = _ => {
      webSocket.onmessage = event => this.messageSubject.next(event.data)
      this.webSocketSubject.next(webSocket)
    }
    return this.webSocketSubject
  }

  getMessages(): Observable<string> {
    const temp = this.messageSubject.pipe(
      concatMap(x => of(x).pipe(delay(500)))
    )
    return temp
  }

  sendMessage(title: string, data: string) {
    this.webSocket.subscribe(webSocket => {
      const message = { title, data }
      webSocket.send(JSON.stringify(message))
    })
  }
}
