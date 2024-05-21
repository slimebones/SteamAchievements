import { Component, OnDestroy, OnInit } from "@angular/core";
import {
  AlertService,
  ClientBus,
  ConnService,
  FcodeCore,
  GotDocUdtoEvt,
  GotDocUdtosEvt,
  LocalStorage,
  OkEvt,
  StorageService,
  log } from "@almazrpe/ngx-kit";
import { Subscription } from "rxjs";
import { ActivatedRoute } from "@angular/router";
import { environment } from "src/environments/environment";
import { UserService } from "./user/user.service";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent implements OnInit, OnDestroy
{
  public title = "client";
  private subs: Subscription[] = [];

  public constructor(
    private alertSv: AlertService,
    private connSv: ConnService,
    private route: ActivatedRoute,
    private storageSv: StorageService,
    private userSv: UserService
  )
  {
  }

  public ngOnInit()
  {
    FcodeCore.ie.secure({
      "got-doc-udtos-evt": GotDocUdtosEvt,
      "got-doc-udto-evt": GotDocUdtoEvt,
      "ok-evt": OkEvt
    });

    this.storageSv.addStorage("local", new LocalStorage());
    this.connSv.init(
      "local",
      undefined,
      environment.serverHost + ":" + environment.serverPort);

    this.subs.push(this.connSv.serverHostPort$.subscribe({
      next: url =>
      {
        log.info(
          `set server url: ${url}`
        );
      }
    }));
    ClientBus.ie.init(this.alertSv, this.connSv);
    this.userSv.init();
  }

  public ngOnDestroy(): void
  {
    for (const sub of this.subs)
    {
      sub.unsubscribe();
    }
  }
}
