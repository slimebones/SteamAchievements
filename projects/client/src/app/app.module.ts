import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { NgxKitModule } from "@almazrpe/ngx-kit";
import { GamesComponent } from "./game/games/games.component";
import { GameComponent } from "./game/game.component";
import { AchievementComponent } from "./achievement/achievement.component";
import { UserComponent } from "./user/user.component";
import { CfgComponent } from "./cfg/cfg.component";

@NgModule({
  declarations: [
    AppComponent,
    GamesComponent,
    GameComponent,
    AchievementComponent,
    UserComponent,
    CfgComponent,
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
