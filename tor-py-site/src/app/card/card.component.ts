import { Component, OnInit, ViewChild, Directive, ViewContainerRef, Input, ComponentFactoryResolver } from '@angular/core';
import { Type } from '@angular/core';

export interface AdComponent {
  data: any;
}

@Component({
  template: `<div>{{data.data}}</div>`
})
export class Test1Component implements AdComponent {
  @Input() data: any;
}

@Component({
  template: `<div>Test2</div><div>{{data.type}}: {{data.temp}}</div><div>abc123</div>`
})
export class Test2Component implements AdComponent {
  @Input() data: any;
}

export class AdItem {
  constructor(public component: Type<any>, public data: any) { }
}

@Directive({
  selector: '[appAdHost]',
})
export class AdDirective {
  constructor(public viewContainerRef: ViewContainerRef) { }
}

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  @ViewChild(AdDirective, { static: true }) adHost: AdDirective;
  @Input() type: any;
  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  ngOnInit() {
    this.loadChild()
  }

  loadChild() {
    const adItem = this.type;

    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(adItem.component);

    const viewContainerRef = this.adHost.viewContainerRef;
    viewContainerRef.clear();

    const componentRef = viewContainerRef.createComponent(componentFactory);
    (componentRef.instance as AdComponent).data = adItem.data;
  }
}
