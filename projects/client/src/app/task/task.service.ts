import { Injectable } from "@angular/core";
import { TaskCreate, TaskUdto } from "../models";
import {
  BusUtils,
  CreateDocReq, DelDocReq, GetDocsReq, UpdDocReq } from "@almazrpe/ngx-kit";
import { Observable } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class TaskService
{
  private readonly Collection = "taskDoc";

  public getMany$(searchq: object): Observable<TaskUdto[]>
  {
    return BusUtils.pubGetDocsReq$(new GetDocsReq({
      collection: this.Collection,
      searchQuery: searchq
    }));
  }

  public create$(data: TaskCreate): Observable<TaskUdto>
  {
    return BusUtils.pubCreateDocReq$(new CreateDocReq({
      collection: this.Collection,
      createQuery: {
        text: data.text
      }
    }));
  }

  public complete$(sid: string): Observable<TaskUdto>
  {
    return BusUtils.pubUpdDocReq$(new UpdDocReq({
      collection: this.Collection,
      searchQuery: {
        sid: sid
      },
      updQuery: {
        "$set": {
          isCompleted: true
        }
      }
    }));
  }

  public redo$(sid: string): Observable<TaskUdto>
  {
    return BusUtils.pubUpdDocReq$(new UpdDocReq({
      collection: this.Collection,
      searchQuery: {
        sid: sid
      },
      updQuery: {
        "$set": {
          isCompleted: false
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
