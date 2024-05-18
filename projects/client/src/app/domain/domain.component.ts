import { Component, OnDestroy, OnInit } from "@angular/core";
import { DomainService } from "./domain.service";
import { StorageService } from "@almazrpe/ngx-kit";
import { Subscription, of, switchMap } from "rxjs";
import { DomainUdto } from "../models";

@Component({
  selector: "app-domain",
  templateUrl: "./domain.component.html",
  styles: [
  ]
})
export class DomainComponent implements OnInit, OnDestroy
{
  public domain?: DomainUdto = undefined;
  private subs: Subscription[] = [];

  public constructor(
    private domainSv: DomainService,
    private storageSv: StorageService)
  {
  }

  public ngOnInit(): void
  {
    this.subs.push(this.storageSv
      .getItem$("local", "selected_domain_sid")
      .pipe(switchMap(sid =>
        {
          if (sid === undefined)
          {
            return of(undefined);
          }
          return this.domainSv.get$({sid: sid});
        }))
      .subscribe({
        next: val =>
        {
          this.domain = val;
        }})
    );
  }

  public ngOnDestroy(): void
  {
    for (let sub of this.subs)
    {
      sub.unsubscribe();
    }
  }
}
