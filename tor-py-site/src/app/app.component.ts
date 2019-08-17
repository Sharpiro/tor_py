import { Component, OnInit } from '@angular/core';
import { TorComponent, GenericComponent } from './card/card.component';
import { SocketService } from './services/socket.service';
import { Type } from '@angular/core';
import { SendVersionsComponent } from './send-versions/send-versions.component';
import { Create2Component } from './create2/create2.component';
import { Created2Component } from './created2/created2.component';
import { Extend2Component } from './extend2/extend2.component';
import { Extended2Component } from './extended2/extended2.component';
import { RelayResolveComponent } from './relay-resolve/relay-resolve.component';
import { RelayResolvedComponent } from './relay-resolved/relay-resolved.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'tor-py-site';
  torComponents: TorComponent[] = []

  constructor(private socketService: SocketService) {
    this.socketService.getMessages().subscribe(message => {
      let component: Type<any>
      let title: string
      switch (message.title) {
        case "sendVersions":
          component = SendVersionsComponent
          title = "Send Versions"
          break;
        case "sendCreate2":
          component = Create2Component
          title = "Send Create2"
          break;
        case "recvCreated2":
          component = Created2Component
          title = "Receive Created2"
          break;
        case "sendExtend2":
          component = Extend2Component
          title = "Send Extend2"
          break;
        case "recvExtended2":
          component = Extended2Component
          title = "Receive Extended2"
          break;
        case "sendRelayResolve":
          component = RelayResolveComponent
          title = "Send Relay Resolve"
          break;
        case "recvRelayResolved":
          component = RelayResolvedComponent
          title = "Receive Relay Resolved"
          break;
        default:
          component = GenericComponent
          title = "Generic Cell"
          break;
      }
      this.torComponents.push(new TorComponent(component, title, message))
    })
  }

  ngOnInit(): void {
    console.log("starting...")
    this.socketService.sendMessage("tor", "")
  }
}
