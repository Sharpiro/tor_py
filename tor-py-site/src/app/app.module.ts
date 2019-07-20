import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { Create2Component } from './create2/create2.component';
import { Created2Component } from './created2/created2.component';
import { CardComponent, AdDirective, Test1Component, Test2Component } from './card/card.component';

@NgModule({
  declarations: [
    AppComponent,
    Create2Component,
    Created2Component,
    CardComponent,
    AdDirective,
    Test1Component,
    Test2Component
  ],
  entryComponents: [Test1Component, Test2Component],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
