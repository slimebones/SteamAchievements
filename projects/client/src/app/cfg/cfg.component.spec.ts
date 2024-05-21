import { ComponentFixture, TestBed } from "@angular/core/testing";

import { CfgComponent } from "./cfg.component";

describe("CfgComponent", () => 
{
  let component: CfgComponent;
  let fixture: ComponentFixture<CfgComponent>;

  beforeEach(async () => 
{
    await TestBed.configureTestingModule({
      declarations: [ CfgComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CfgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => 
{
    expect(component).toBeTruthy();
  });
});
