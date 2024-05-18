import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { NgxKitModule } from "@almazrpe/ngx-kit";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxKitModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
