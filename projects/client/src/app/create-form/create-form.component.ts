import { InputType } from "@almazrpe/ngx-kit";
import {
  Component,
  ElementRef, EventEmitter, OnInit, Output, ViewChild } from "@angular/core";
import { FormControl, FormGroup } from "@angular/forms";

@Component({
  selector: "app-create-form",
  templateUrl: "./create-form.component.html",
  styles: [
  ]
})
export class CreateFormComponent implements OnInit
{
  @Output()
  public onCreate: EventEmitter<string> = new EventEmitter();

  @ViewChild("inp", {read: ElementRef})
  private inp: ElementRef;

  public InputType = InputType;
  public form: FormGroup;

  public ngOnInit(): void
  {
    this.form = new FormGroup({
      name: new FormControl("")
    });
  }

  public onSubmit()
  {
    this.inp.nativeElement.querySelector("input").focus();
    const name = this.form.value.name.trim();
    if (name === "")
    {
      return;
    }
    this.onCreate.emit(name);
    this.form.setValue({name: ""});
  }

  public onKeydownEnter()
  {
    this.onSubmit();
  }
}
