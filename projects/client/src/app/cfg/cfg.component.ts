import { Component, OnInit } from "@angular/core";
import { UserService } from "../user/user.service";
import { Observable } from "rxjs";
import { UserUdto } from "../user/models";
import { FormControl, FormGroup } from "@angular/forms";

@Component({
  selector: "app-cfg",
  templateUrl: "./cfg.component.html",
  styles: [
  ]
})
export class CfgComponent implements OnInit
{
  public user$: Observable<UserUdto | null>;
  public usernameForm: FormGroup;
  public platformForm: FormGroup;

  public constructor(private userSv: UserService)
  {
  }

  public ngOnInit()
  {
    this.user$ = this.userSv.getCurrentUser$();
    this.usernameForm = new FormGroup({
      username: new FormControl("")
    });
    this.platformForm = new FormGroup({
      platform: new FormControl(""),
      platformUserSid: new FormControl(""),
      token: new FormControl("")
    });
  }

  public onSubmitUsername()
  {
    this.userSv.setUser(this.usernameForm.controls["username"].value);
  }

  public onSubmitPlatform()
  {
    this.userSv.registerPlatform(
      this.platformForm.controls["platform"].value,
      this.platformForm.controls["platformUserSid"].value,
      this.platformForm.controls["token"].value
    );
  }

  public sync()
  {
    this.userSv.sync();
  }
}
