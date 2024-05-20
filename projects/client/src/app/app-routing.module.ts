import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { GamesComponent } from "./game/games/games.component";

const routes: Routes = [
  {
    path: "**",
    component: GamesComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
