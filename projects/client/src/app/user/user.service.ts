import {
  BusUtils,
  ClientBus,
  GetDocsReq,
  GotDocUdtoEvt, StorageService} from "@almazrpe/ngx-kit";
import { Injectable } from "@angular/core";
import { Observable, map, of, switchMap, take } from "rxjs";
import {
  RegisterOrLoginUserReq,
  RegisterPlatformReq, SyncReq, UserUdto } from "./models";

@Injectable({
  providedIn: "root"
})
export class UserService
{
  private currentUserSid$: Observable<string | null>;

  public constructor(
    private storageSv: StorageService
  )
  {
  }

  public init()
  {
    this.currentUserSid$ = this.storageSv.initItem$(
      "local", "current_user_sid", "");
  }

  public getCurrentUser$(): Observable<UserUdto | null>
  {
    return this.currentUserSid$.pipe(
      switchMap(userSid =>
      {
        if (userSid === null)
        {
          return of(null);
        }
        return BusUtils.pubGetDocReq$<UserUdto>(new GetDocsReq({
          searchQuery: {sid: userSid},
          collection: "user_doc"
        }));
      }));
  }

  public registerPlatform(
    platform: string, platformUserSid: string, token: string)
  {
    this.getCurrentUser$().pipe(
      switchMap(user =>
      {
        if (user === null)
        {
          throw new Error("unset user");
        }
        return ClientBus.ie.pub$(new RegisterPlatformReq({
          user_sid: user.sid,
          platform: platform,
          platform_user_sid: platformUserSid,
          token: token
        }));
      }),
      take(1)
    ).subscribe();
  }

  public setUser(username: string)
  {
    ClientBus.ie.pub$(new RegisterOrLoginUserReq({
          username: username
        }))
      .pipe(map(rae =>
        {
          const user = (rae.evt as GotDocUdtoEvt<UserUdto>).udto;
          this.storageSv.setItemVal("local", "current_user_sid", user.sid);
        }))
      .subscribe();
  }

  public sync()
  {
    return this.currentUserSid$.pipe(
        switchMap(userSid =>
        {
          if (userSid === null)
          {
            throw new Error("unset user sid");
          }
          return ClientBus
            .ie
            .pub$(new SyncReq({user_sid: userSid}))
            .pipe(map(_ => {}));
        }))
      .subscribe();
  }
}
