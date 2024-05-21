import { BusUtils, GetDocsReq } from "@almazrpe/ngx-kit";
import { Component, OnInit } from "@angular/core";
import { Observable, of, switchMap } from "rxjs";
import { UserService } from "src/app/user/user.service";
import { GameUdto } from "../models";

@Component({
  selector: "app-games",
  templateUrl: "./games.component.html",
  styles: [
  ]
})
export class GamesComponent implements OnInit
{
  public games$: Observable<GameUdto[]>;

  public constructor(private userSv: UserService)
  {
  }

  public ngOnInit(): void
  {
    this.games$ = this.userSv.getCurrentUser$().pipe(
      switchMap(user =>
      {
        if (user === null)
        {
          return of([]);
        }
        return BusUtils.pubGetDocsReq$<GameUdto>(new GetDocsReq({
          collection: "game_doc",
          searchQuery: {sid: {$in: user.game_sids}}
        }));
      }));
  }
}
