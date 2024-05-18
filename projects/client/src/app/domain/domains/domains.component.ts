import { Component, OnDestroy, OnInit } from "@angular/core";
import { DomainUdto } from "src/app/models";
import { DomainService } from "../domain.service";
import { Observable, Subscription } from "rxjs";
import { StorageService } from "@almazrpe/ngx-kit";

@Component({
  selector: "app-domains",
  templateUrl: "./domains.component.html",
  styles: [
  ]
})
export class DomainsComponent implements OnInit, OnDestroy
{
  public domains: DomainUdto[] = [];
  public subs: Subscription[] = [];

  private selectedDomainSid$: Observable<string>;

  public constructor(
    private domainSv: DomainService,
    private storageSv: StorageService
  )
  {
  }

  public ngOnInit()
  {
    this.storageSv.addItem("local", "selected_domain_sid");
    this.selectedDomainSid$ = this.storageSv.initItem$(
      "local", "selected_domain_sid", this.tryGetDefaultSelectedDomainSid());

    this.subs.push(this.domainSv.getMany$().subscribe({
      next: val =>
      {
        this.domains = val;
      }
    }));
  }

  public onCreate(name: string)
  {
    this.domainSv.create$({
      name: name,
      color_palette: {
        c60_fg: "FFFFFF",
        c30_fg: "FFFFFF",
        c10_fg: "FFFFFF",
        c60_bg: "C40C0C",
        c30_bg: "FF8A08",
        c10_bg: "FFC100"
      }
    }).subscribe({
      next: val =>
      {
        this.domains.splice(0, 0, val);
      }
    });
  }

  private tryGetDefaultSelectedDomainSid(): string | undefined
  {
    if (this.domains.length > 0)
    {
      return this.domains[0].sid;
    }
    return undefined;
  }

  public ngOnDestroy()
  {
    for (let sub of this.subs)
    {
      sub.unsubscribe();
    }
  }

  public selectDomain(domain: DomainUdto): void
  {
    this.storageSv.setItemVal(
      "local",
      "selected_domain_sid",
      domain.sid);
  }

  public getEntrySelectors(domain: DomainUdto): string[]
  {
    if (this.storageSv.getItem("local", "selected_domain_sid") === domain.sid)
    {
      return ["underline"];
    }
    return [];
  }
}
