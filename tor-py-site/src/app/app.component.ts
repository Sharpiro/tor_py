import { Component, OnInit } from '@angular/core';
import { AdItem, Test1Component, Test2Component } from './card/card.component';
import { SocketService } from './services/socket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'tor-py-site';
  cards: AdItem[] = [
    // new AdItem(Test1Component, { data: 'test123', bio: 'Brave as they come' }),
    // new AdItem(Test2Component, { type: 'bro', temp: 'whatever' })
  ]
  messages: string[] = []

  constructor(private socketService: SocketService) {
    this.socketService.getMessages().subscribe(val => {
      this.cards.push(new AdItem(Test1Component, { data: val }))
      // this.messages.push(val)
      // console.log(val)
    })
  }

  ngOnInit(): void {
    console.log("starting...")
    this.socketService.sendMessage("tor", "the data 1")
  }
}
