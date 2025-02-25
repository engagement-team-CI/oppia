// Copyright 2017 The Oppia Authors. All Rights Reserved.
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
 * @fileoverview Directive for the hint editor.
 */

require(
  'components/forms/schema-based-editors/schema-based-editor.directive.ts');
require('directives/angular-html-bind.directive.ts');

require('domain/utilities/url-interpolation.service.ts');
require(
  'components/state-editor/state-editor-properties-services/' +
  'state-property.service.ts');
require('services/context.service.ts');
require('services/editability.service.ts');
require('services/external-save.service.ts');

import { Subscription } from 'rxjs';

angular.module('oppia').directive('hintEditor',
  function() {
    return {
      restrict: 'E',
      scope: {},
      bindToController: {
        hint: '=',
        getIndexPlusOne: '&indexPlusOne',
        getOnSaveFn: '&onSave',
        showMarkAllAudioAsNeedingUpdateModalIfRequired: '='
      },
      template: require(
        'components/state-directives/hint-editor/hint-editor.directive.html'),
      controllerAs: '$ctrl',
      controller: [
        'ContextService', 'EditabilityService',
        'ExternalSaveService', 'StateHintsService',
        function(
            ContextService, EditabilityService,
            ExternalSaveService, StateHintsService) {
          var ctrl = this;
          ctrl.directiveSubscriptions = new Subscription();
          ctrl.openHintEditor = function() {
            if (ctrl.isEditable) {
              ctrl.hintMemento = angular.copy(ctrl.hint);
              ctrl.hintEditorIsOpen = true;
            }
          };

          ctrl.saveThisHint = function() {
            ctrl.hintEditorIsOpen = false;
            var contentHasChanged = (
              ctrl.hintMemento.hintContent.html !==
              ctrl.hint.hintContent.html);
            ctrl.hintMemento = null;
            if (contentHasChanged) {
              var hintContentId = ctrl.hint.hintContent.contentId;
              ctrl.showMarkAllAudioAsNeedingUpdateModalIfRequired(
                [hintContentId]);
            }
            ctrl.getOnSaveFn()();
          };

          ctrl.cancelThisHintEdit = function() {
            ctrl.hint.hintContent =
              angular.copy(ctrl.hintMemento.hintContent);
            ctrl.hintMemento = null;
            ctrl.hintEditorIsOpen = false;
          };

          ctrl.$onInit = function() {
            ctrl.directiveSubscriptions.add(
              ExternalSaveService.onExternalSave.subscribe(() => {
                if (ctrl.hintEditorIsOpen &&
                      ctrl.editHintForm.$valid) {
                  ctrl.saveThisHint();
                }
              }));
            ctrl.isEditable = EditabilityService.isEditable();
            ctrl.StateHintsService = StateHintsService;
            ctrl.editHintForm = {};
            ctrl.hintEditorIsOpen = false;

            ctrl.HINT_FORM_SCHEMA = {
              type: 'html',
              ui_config: {
                hide_complex_extensions: (
                  ContextService.getEntityType() === 'question')
              }
            };

            ctrl.hintMemento = null;
          };
          ctrl.$onDestroy = function() {
            ctrl.directiveSubscriptions.unsubscribe();
          };
        }
      ]
    };
  });
