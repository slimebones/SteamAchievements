import { Component, OnDestroy, OnInit } from "@angular/core";
import { BehaviorSubject, Subscription } from "rxjs";
import { TimingService } from "./timing.service";
import { TimerGroupUdto, TimerUdto } from "./models";

@Component({
  selector: "app-timing",
  templateUrl: "./timing.component.html",
  styles: [
  ]
})
export class TimingComponent implements OnInit, OnDestroy
{
  public nextGroupName: number = 1;
  public isEnabled: boolean = true;
  public toggleBtnSelectors$: BehaviorSubject<string[]> =
    new BehaviorSubject(["filter-white"]);

  public groupToTimers: Map<TimerGroupUdto, TimerUdto[]> = new Map();

  public selectedGroupSid?: string = undefined;
  public selectedTimers?: TimerUdto[] = undefined;

  private subs: Subscription[] = [];

  public readonly BASIC_GROUP_SELECTOR_CLASSES: string[] = [
    "border", "rounded"
  ];
  public readonly SELECTED_GROUP_SELECTOR_CLASSES: string[] = [
    ...this.BASIC_GROUP_SELECTOR_CLASSES,
    "bg-c10-bg"
  ];
  public readonly UNSELECTED_GROUP_SELECTOR_CLASSES: string[] = [
    ...this.BASIC_GROUP_SELECTOR_CLASSES,
    "hover:bg-c10-bg-active"
  ];

  public constructor(
    private timingSv: TimingService
  )
  {
  }

  public ngOnInit(): void
  {
    this.subs.push(this.timingSv.getGroupsToTimers$().subscribe({
      next: _map =>
      {
        this.groupToTimers = _map;
        for (let group of this.groupToTimers.keys())
        {
          this.nextGroupName++;
        }
      }
    }));
  }

  public ngOnDestroy(): void
  {
    for (let sub of this.subs)
    {
      sub.unsubscribe();
    }
  }

  public toggleTiming()
  {
    this.isEnabled = !this.isEnabled;
    this.isEnabled
      ? this.toggleBtnSelectors$.next(["filter-gray"])
      : this.toggleBtnSelectors$.next(["filter-white"]);
  }

  public createGroup()
  {
    this.timingSv.createGroup$(this.nextGroupName.toString()).subscribe({
      next: group => {this.groupToTimers.set(group, []);}
    });
  }

  public selectGroup(group: TimerGroupUdto)
  {
    this.selectedGroupSid = group.sid;
    this.selectedTimers = this.groupToTimers.get(group);
    this.groupToTimers.set(group, this.selectedTimers ?? []);
  }
}
