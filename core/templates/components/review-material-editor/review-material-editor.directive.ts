// Copyright 2018 The Oppia Authors. All Rights Reserved.
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

import { SubtitledHtml } from 'domain/exploration/subtitled-html.model';

/**
 * @fileoverview Directive for the skill review material editor.
 */

require(
  'components/forms/schema-based-editors/schema-based-editor.directive.ts');
require('domain/utilities/url-interpolation.service.ts');
require('components/ck-editor-helpers/ck-editor-4-rte.component.ts');
require('components/ck-editor-helpers/ck-editor-4-widgets.initializer.ts');
require('components/forms/custom-forms-directives/image-uploader.component.ts');

require('directives/mathjax-bind.directive.ts');
require('filters/string-utility-filters/normalize-whitespace.filter.ts');

require('objects/objectComponentsRequires.ts');

require('directives/angular-html-bind.directive.ts');

angular.module('oppia').directive('reviewMaterialEditor', [
  function() {
    return {
      restrict: 'E',
      scope: {},
      bindToController: {
        getBindableDict: '&bindableDict',
        onSaveExplanation: '='
      },
      template: require(
        'components/review-material-editor/' +
        'review-material-editor.directive.html'),
      controllerAs: '$ctrl',
      controller: [
        'COMPONENT_NAME_EXPLANATION',
        function(
            COMPONENT_NAME_EXPLANATION) {
          var ctrl = this;
          var explanationMemento = null;

          ctrl.openConceptCardExplanationEditor = function() {
            ctrl.editableExplanation =
              ctrl.getBindableDict().displayedConceptCardExplanation;
            explanationMemento = ctrl.editableExplanation;
            ctrl.conceptCardExplanationEditorIsShown = true;
          };

          ctrl.closeConceptCardExplanationEditor = function() {
            ctrl.editableExplanation = explanationMemento;
            ctrl.conceptCardExplanationEditorIsShown = false;
          };

          ctrl.saveConceptCardExplanation = function() {
            ctrl.conceptCardExplanationEditorIsShown = false;
            var explanationObject = SubtitledHtml.createDefault(
              ctrl.editableExplanation, COMPONENT_NAME_EXPLANATION);
            ctrl.onSaveExplanation(explanationObject);
          };
          ctrl.$onInit = function() {
            ctrl.HTML_SCHEMA = {
              type: 'html'
            };
            ctrl.editableExplanation =
              ctrl.getBindableDict().displayedConceptCardExplanation;
            ctrl.conceptCardExplanationEditorIsShown = false;
          };
        }
      ]
    };
  }
]);
