import { Component, ElementRef, OnInit, ViewChild } from "@angular/core";
import { ProjectUdto } from "src/app/models";
import { ProjectService } from "../project.service";
import { FormControl, FormGroup } from "@angular/forms";
import { InputType, StorageService, asrt } from "@almazrpe/ngx-kit";
import { Subscription } from "rxjs";

@Component({
  selector: "app-projects",
  templateUrl: "./projects.component.html",
  styles: [
  ]
})
export class ProjectsComponent implements OnInit
{
  @ViewChild("project_create_inp", {read: ElementRef})
  private projectCreateInp: ElementRef;

  public InputType = InputType;

  public projects: ProjectUdto[] = [];
  public projectCreateForm: FormGroup;
  private subs: Subscription[] = [];

  public constructor(
    private projectSv: ProjectService,
    private storageSv: StorageService)
  {}

  public ngOnInit(): void
  {
    this.projectSv.getMany$().subscribe({next: val =>
      {
        this.projects = val;

        // select first project if nothing selected - later might want to
        // toggle this via the settings
        if (
          this.projects.length > 0
          && this.projectSv.getCurrentProjectSid() === null)
        {
          this.selectProject(this.projects[0]);
        }
      }});
    this.projectCreateForm = new FormGroup({
      name: new FormControl("")
    });
  }

  public ngOnDestroy(): void
  {
    for (const sub of this.subs)
    {
      sub.unsubscribe();
    }
  }

  public onKeydownEnter(): void
  {
    this.onProjectCreateSubmit();
  }

  private getDistilledProjectNameInput(): string
  {
    return this.projectCreateForm.value.name.trim();
  }

  public onProjectCreateSubmit(): void
  {
    this.projectCreateInp.nativeElement.querySelector("input").focus();
    const name = this.getDistilledProjectNameInput();
    if (name === "")
    {
      return;
    }
    this.projectSv.create$({name: name}).subscribe({
      next: val => this.projects.splice(0, 0, val)});
    this.projectCreateForm.setValue({name: ""});
  }

  public selectProject(project: ProjectUdto): void
  {
    this.projectSv.setCurrentProject(project);
  }

  public getProjectSelectors(project: ProjectUdto): string[]
  {
    if (this.projectSv.getCurrentProjectSid() === project.sid)
    {
      return ["underline"];
    }
    return [];
  }

  public del(project: ProjectUdto): void
  {
    this.projectSv.del$(project.sid).subscribe({
      next: _ =>
      {
        const deldIndex = this.projects.findIndex(v => v.sid == project.sid);
        if (this.projectSv.getCurrentProjectSid() === project.sid)
        {
          this.projectSv.setCurrentProject(null);
        }
        if (deldIndex === undefined)
        {
          asrt.fail();
          throw new Error();
        }
        this.projects.splice(deldIndex, 1);
        const audio = new Audio(
          "http://"
          + this.storageSv.getItem("local", "conn_hostport")
          + "/share/fire_hurt3.ogg");
        audio.play();
      }});
  }
}
