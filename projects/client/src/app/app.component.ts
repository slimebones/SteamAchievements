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
import { Observable, Subscription, map } from "rxjs";
import { ActivatedRoute } from "@angular/router";
import { environment } from "src/environments/environment";
import { ProjectService } from "./project/project.service";
import { ViewType, ViewData } from "./models";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent implements OnInit, OnDestroy
{
  public AppView = ViewType;

  public title = "client";
  public openedViewType$: Observable<ViewType>;
  private readonly UnselectedViewCssSelectors: string[] = ["hover:underline"];
  private readonly SelectedViewCssSelectors: string[] = ["underline"];
  public views: ViewData[] = [
    {
      title: "Tasks",
      type: ViewType.TPI,
      cssSelectors: this.UnselectedViewCssSelectors
    },
    {
      title: "Ideas",
      type: ViewType.Ideas,
      cssSelectors: this.UnselectedViewCssSelectors
    },
    {
      title: "Events",
      type: ViewType.Events,
      cssSelectors: this.UnselectedViewCssSelectors
    },
    {
      title: "Domains",
      type: ViewType.Domains,
      cssSelectors: this.UnselectedViewCssSelectors
    },
  ];
  private subs: Subscription[] = [];

  public constructor(
    private alertSv: AlertService,
    private connSv: ConnService,
    private route: ActivatedRoute,
    private storageSv: StorageService,
    private projectSv: ProjectService
  )
  {
  }

  public ngOnInit()
  {
    // maybe redundant: problem probably was with incorrect dockerfile setup
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
    this.projectSv.init();
    this.openedViewType$ = this.storageSv.addItem$(
        "local", "opened_view_type")
      .pipe(
        map(val =>
        {
          return val as ViewType;
        })
      );
    this.storageSv.getItem("local", "opened_view_type", "tpi");

    this.subs.push(this.openedViewType$.subscribe({
      next: val =>
      {
        for (let view of this.views)
        {
          if (view.type === val)
          {
            view.cssSelectors = this.SelectedViewCssSelectors;
            continue;
          }
          view.cssSelectors = this.UnselectedViewCssSelectors;
        }
      }
    }));

    this.subs.push(this.connSv.serverHostPort$.subscribe({
      next: url =>
      {
        log.info(
          `set server url: ${url}`
        );
      }
    }));
    ClientBus.ie.init(this.alertSv, this.connSv);
  }

  public ngOnDestroy(): void
  {
    for (const sub of this.subs)
    {
      sub.unsubscribe();
    }
  }

  private setOpenedViewType(viewType: ViewType)
  {
    this.storageSv.setItemVal(
      "local", "opened_view_type", viewType.toString());
  }

  public selectView(view: ViewData): void
  {
    this.setOpenedViewType(view.type);
  }
}
