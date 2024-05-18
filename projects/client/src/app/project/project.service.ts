import { Injectable } from "@angular/core";
import { ProjectCreate, ProjectUdto } from "../models";
import {
  BusUtils,
  CreateDocReq,
  DelDocReq,
  GetDocsReq,
  Query,
  StorageService,
  UpdDocReq } from "@almazrpe/ngx-kit";
import { Observable, map, of, switchMap } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class ProjectService
{
  public currentProject$: Observable<ProjectUdto | null>;

  private readonly Collection = "projectDoc";

  public constructor(
    private storageSv: StorageService
  )
  {
  }

  public init()
  {
    this.currentProject$ = this.storageSv.addItem$<string | null>(
        "local", "current_project_sid")
      .pipe(switchMap(sid => this.parseProject$(sid)));
  }

  public getCurrentProjectSid(): string | null
  {
    let val = this.storageSv.getItem(
      "local", "current_project_sid", null);
    if (val === "null" || val === "")
    {
      val = null;
    }
    return val;
  }

  private parseProject$(
    sid: string | null): Observable<ProjectUdto | null>
  {
    if (sid == null)
    {
      return of(null);
    }
    return this.get$({sid: sid});
  }

  public get$(searchq: Query = {}): Observable<ProjectUdto>
  {
    return this.getMany$(searchq).pipe(map(val => val[0]));
  }

  public setCurrentProject(project: ProjectUdto | null)
  {
    this.storageSv.setItemVal(
      "local", "current_project_sid", project?.sid);
  }

  public getMany$(searchq: object = {}): Observable<ProjectUdto[]>
  {
    return BusUtils.pubGetDocsReq$(new GetDocsReq({
      collection: this.Collection,
      searchQuery: searchq
    }));
  }

  public create$(data: ProjectCreate): Observable<ProjectUdto>
  {
    return BusUtils.pubCreateDocReq$(new CreateDocReq({
      collection: this.Collection,
      createQuery: {
        name: data.name
      }
    }));
  }

  public attachTask$(
    projectSid: string, taskSid: string): Observable<ProjectUdto>
  {
    return BusUtils.pubUpdDocReq$(new UpdDocReq({
      collection: this.Collection,
      searchQuery: {
        sid: projectSid
      },
      updQuery: {
        "$push": {
          taskSids: taskSid
        }
      }
    }));
  }

  public del$(sid: string): Observable<void>
  {
    return BusUtils.pubDelDocReq$(new DelDocReq({
      collection: this.Collection,
      searchQuery: {
        sid: sid
      }
    }));
  }
}
