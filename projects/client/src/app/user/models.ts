import { Req, Udto, code } from "@almazrpe/ngx-kit";

export interface UserUdto extends Udto
{
  username: string;
  global_completion: number;
  registered_platforms: string[];
  platform_to_user_sid: {[platform: string]: string | null};
  platform_to_api_token: {[platform: string]: string | null};
  game_sids: string[];
}

@code("register_platform_req")
export class RegisterPlatformReq extends Req
{
  public user_sid: string;
  public platform: string;
  public platform_user_sid: string;
  public token: string;

  public constructor(args: any)
  {
    super(args);
    this.user_sid = args.user_sid;
    this.platform = args.platform;
    this.platform_user_sid = args.platform_user_sid;
    this.token = args.token;
  }
}

@code("register_or_login_user_req")
export class RegisterOrLoginUserReq extends Req
{
  public username: string;

  public constructor(args: any)
  {
    super(args);
    this.username = args.username;
  }
}

@code("deregister_platform_req")
export class DeregisterPlatformReq extends Req
{
  public user_sid: string;
  public platform: string;

  public constructor(args: any)
  {
    super(args);
    this.user_sid = args.user_sid;
    this.platform = args.platform;
  }
}

/**
 * Syncs data for a user with all platforms' APIs.
 */
@code("sync_req")
export class SyncReq extends Req
{
  public user_sid: string;

  public constructor(args: any)
  {
    super(args);
    this.user_sid = args.user_sid;
  }
}
