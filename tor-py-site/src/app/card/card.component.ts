import { Component, OnInit, ViewChild, Directive, ViewContainerRef, Input, ComponentFactoryResolver } from '@angular/core';
import { Type } from '@angular/core';
import { Message } from '../services/socket.service';

export interface CommandComponent {
  data: any;
}

export class TorComponent {
  constructor(public component: Type<any>, public message: Message) { }
}

@Component({
  template: '<div>{{stringData}}</div>'
})
export class GenericComponent implements CommandComponent, OnInit {
  data: any;
  stringData: string

  ngOnInit(): void {
    this.stringData = JSON.stringify(this.data)
  }
}

@Directive({
  selector: '[appTorComponentHost]',
})
export class TorComponentDirective {
  constructor(public viewContainerRef: ViewContainerRef) { }
}

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  @ViewChild(TorComponentDirective, { static: true }) torComponentHost: TorComponentDirective;
  @Input() torComponent: TorComponent;
  private showRawPayload = false

  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  ngOnInit() {
    this.loadChild()
  }

  toggleRawPayload() {
    this.showRawPayload = !this.showRawPayload
  }

  loadChild() {
    const torComponent = this.torComponent;

    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(torComponent.component);

    const viewContainerRef = this.torComponentHost.viewContainerRef;
    viewContainerRef.clear();

    const componentRef = viewContainerRef.createComponent(componentFactory);
    (componentRef.instance as CommandComponent).data = torComponent.message.data;
  }
}
