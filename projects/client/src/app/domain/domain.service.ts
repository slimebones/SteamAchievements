import {
  BusUtils, CreateDocReq, DelDocReq, GetDocsReq, Query, UpdDocReq
} from "@almazrpe/ngx-kit";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { DomainCreate, DomainUdto } from "../models";

@Injectable({
  providedIn: "root"
})
export class DomainService
{
  private readonly Collection = "focusDomainDoc";

  public get$(searchq: Query): Observable<DomainUdto>
  {
    return BusUtils.pubGetDocReq$(new GetDocsReq({
      collection: this.Collection,
      searchQuery: searchq}));
  }

  public getMany$(searchq: Query = {}): Observable<DomainUdto[]>
  {
    return BusUtils.pubGetDocsReq$(new GetDocsReq({
      collection: this.Collection,
      searchQuery: searchq}));
  }

  public upd$(searchq: Query, updq: Query): Observable<DomainUdto>
  {
    return BusUtils.pubUpdDocReq$(new UpdDocReq({
      collection: this.Collection,
      searchQuery: searchq,
      updQuery: updq
    }));
  }

  public create$(createq: DomainCreate): Observable<DomainUdto>
  {
    return BusUtils.pubCreateDocReq$(new CreateDocReq({
      collection: this.Collection,
      createQuery: createq
    }));
  }

  public del$(searchq: Query): Observable<void>
  {
    return BusUtils.pubDelDocReq$(new DelDocReq({
      collection: this.Collection,
      searchQuery: searchq
    }));
  }
}
