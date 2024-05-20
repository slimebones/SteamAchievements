import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { NgxKitModule } from "@almazrpe/ngx-kit";
import { GamesComponent } from './games/games.component';
import { GameComponent } from './games/game/game.component';
import { AchievementComponent } from './achievement/achievement.component';

@NgModule({
  declarations: [
    AppComponent,
    GamesComponent,
    GameComponent,
    AchievementComponent,
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
