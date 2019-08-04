import { Component, OnInit, ViewChild, Directive, ViewContainerRef, Input, ComponentFactoryResolver } from '@angular/core';
import { Type } from '@angular/core';
import { Message } from '../services/socket.service';

export interface CommandComponent {
  data: any;
}

export class TorComponent {
  constructor(public component: Type<any>, public title: string, public message: Message) { }
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
  showRawPayload = false
  title: string
  isVisible = false;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  ngOnInit() {
    this.title = this.torComponent.title
    // this.loadChild()
    // setTimeout(() => {
    //   this.clearChild()
    // }, 2000);
    // setTimeout(() => {
    //   this.loadChild()
    // }, 5000);
  }

  toggleVisibility() {
    if (!this.isVisible) {
      this.loadChild()
    } else {
      this.clearChild()
    }
    this.isVisible = !this.isVisible
    // console.log(this.isVisible)
    // setTimeout(() => {
    //   this.loadChild()
    // }, 5000);
  }

  toggleRawPayload() {
    this.showRawPayload = !this.showRawPayload
  }

  loadChild() {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.torComponent.component);

    const viewContainerRef = this.torComponentHost.viewContainerRef;
    viewContainerRef.clear();

    const componentRef = viewContainerRef.createComponent(componentFactory);
    (componentRef.instance as CommandComponent).data = this.torComponent.message.data;
  }


  clearChild() {
    const viewContainerRef = this.torComponentHost.viewContainerRef;
    viewContainerRef.clear();
  }
}
