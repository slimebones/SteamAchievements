import { Component } from "@angular/core";
import { UserService } from "../user/user.service";

@Component({
  selector: "app-cfg",
  templateUrl: "./cfg.component.html",
  styles: [
  ]
})
export class CfgComponent
{
  public constructor(public userSv: UserService)
  {
  }
}
