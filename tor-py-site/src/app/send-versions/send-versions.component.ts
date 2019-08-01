import { Component, OnInit } from '@angular/core';
import { CommandComponent } from '../card/card.component';

@Component({
  selector: 'app-send-versions',
  templateUrl: './send-versions.component.html',
  styleUrls: ['./send-versions.component.css']
})
export class SendVersionsComponent implements CommandComponent, OnInit {
  data: VersionsData;

  ngOnInit(): void { }
}

interface VersionsData {
  payload: Payload
}

interface Payload {
  versions: number[]
}
