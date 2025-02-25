// Copyright 2019 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Module for the classroom page.
 */

import { APP_INITIALIZER, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { RequestInterceptor } from 'services/request-interceptor.service';
import { SharedComponentsModule } from 'components/shared-component.module';
import { platformFeatureInitFactory, PlatformFeatureService } from
  'services/platform-feature.service';
import { ClassroomPageComponent } from './classroom-page.component';
import { TopicSummaryTileComponent } from
  'components/summary-tile/topic-summary-tile.component';
import { ClassroomPageRootComponent } from './classroom-page-root.component';

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    SharedComponentsModule
  ],
  declarations: [
    ClassroomPageComponent,
    ClassroomPageRootComponent,
    TopicSummaryTileComponent
  ],
  entryComponents: [
    ClassroomPageComponent,
    ClassroomPageRootComponent,
    TopicSummaryTileComponent
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: RequestInterceptor,
      multi: true
    },
    {
      provide: APP_INITIALIZER,
      useFactory: platformFeatureInitFactory,
      deps: [PlatformFeatureService],
      multi: true
    }
  ],
  bootstrap: [ClassroomPageRootComponent]
})
export class ClassroomPageModule {}
