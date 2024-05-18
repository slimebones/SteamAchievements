import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { ProjectComponent } from "./project/project.component";
import { TaskComponent } from "./task/task.component";
import { ProjectsComponent } from "./project/projects/projects.component";
import { TasksComponent } from "./task/tasks/tasks.component";
import { NgxKitModule } from "@almazrpe/ngx-kit";
import { ReactiveFormsModule } from "@angular/forms";
import { DomainComponent } from './domain/domain.component';
import { DomainsComponent } from './domain/domains/domains.component';
import { DomainManagerComponent } from './domain/domain-manager/domain-manager.component';
import { CreateFormComponent } from './create-form/create-form.component';
import { TimingComponent } from './timing/timing.component';

@NgModule({
  declarations: [
    AppComponent,
    ProjectComponent,
    TaskComponent,
    ProjectsComponent,
    TasksComponent,
    DomainComponent,
    DomainsComponent,
    DomainManagerComponent,
    CreateFormComponent,
    TimingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxKitModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
