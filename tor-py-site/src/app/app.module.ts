import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { Create2Component } from './create2/create2.component';
import { Created2Component } from './created2/created2.component';
import { CardComponent, TorComponentDirective, GenericComponent } from './card/card.component';
import { SOCKET_URL } from './services/socket.service';
import { environment } from 'src/environments/environment';
import { SendVersionsComponent } from './send-versions/send-versions.component';
import { Extend2Component } from './extend2/extend2.component';
import { Extended2Component } from './extended2/extended2.component';
import { RelayResolveComponent } from './relay-resolve/relay-resolve.component';

@NgModule({
  declarations: [
    AppComponent,
    Created2Component,
    CardComponent,
    TorComponentDirective,
    SendVersionsComponent,
    Create2Component,
    GenericComponent,
    Extend2Component,
    Extended2Component,
    RelayResolveComponent
  ],
  entryComponents: [
    SendVersionsComponent,
    Create2Component,
    GenericComponent,
    Created2Component,
    Extend2Component,
    Extended2Component,
    RelayResolveComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [
    { provide: SOCKET_URL, useValue: environment.socketHostAndPort }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
