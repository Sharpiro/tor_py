import { Component, OnInit } from '@angular/core';
import { TorComponent, GenericComponent } from './card/card.component';
import { SocketService } from './services/socket.service';
import { Type } from '@angular/core';
import { SendVersionsComponent } from './send-versions/send-versions.component';
import { Create2Component } from './create2/create2.component';

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
      switch (message.title) {
        case "sendVersions":
          component = SendVersionsComponent
          break;
        case "sendCreate2":
          component = Create2Component
          break;
        default:
          component = GenericComponent
          break;
      }
      this.torComponents.push(new TorComponent(component, message))
    })
  }

  ngOnInit(): void {
    console.log("starting...")
    this.socketService.sendMessage("tor", "")
  }
}
