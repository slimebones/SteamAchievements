import { BusUtils, ClientBus, GetDocsReq } from "@almazrpe/ngx-kit";
import { Injectable } from "@angular/core";
import { Observable, map } from "rxjs";
import { SyncReq, UserUdto } from "./models";

@Injectable({
  providedIn: "root"
})
export class UserService
{
  private currentUserSid: string | null = null;

  public constructor() { }

  public setUser(username: string)
  {
    BusUtils.pubGetDocReq$<UserUdto>(new GetDocsReq({
        searchQuery: {username: username}
      }))
      .pipe(
        map());
    this.currentUserSid = sid;
  }

  public sync$(): Observable<void>
  {
    if (this.currentUserSid === null)
    {
      throw new Error("unset user sid");
    }
    return ClientBus
      .ie
      .pub$(new SyncReq({user_sid: this.currentUserSid}))
      .pipe(map(_ => {}));
  }
}
