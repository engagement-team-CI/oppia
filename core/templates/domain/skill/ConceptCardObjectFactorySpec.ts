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

/**
 * @fileoverview Unit tests for ConceptCardObjectFactory.
 */

import { TestBed } from '@angular/core/testing';

import { ConceptCardBackendDict, ConceptCardObjectFactory } from 'domain/skill/ConceptCardObjectFactory';
import { SubtitledHtml } from 'domain/exploration/subtitled-html.model';
import { WorkedExampleBackendDict, WorkedExampleObjectFactory } from 'domain/skill/WorkedExampleObjectFactory';
import { RecordedVoiceovers } from 'domain/exploration/recorded-voiceovers.model';

describe('Concept card object factory', () => {
  let conceptCardObjectFactory: ConceptCardObjectFactory;
  let conceptCardDict: ConceptCardBackendDict;
  let example1: WorkedExampleBackendDict;
  let example2: WorkedExampleBackendDict;
  let workedExampleObjectFactory: WorkedExampleObjectFactory;

  beforeEach(() => {
    conceptCardObjectFactory = TestBed.inject(ConceptCardObjectFactory);
    workedExampleObjectFactory = TestBed.inject(WorkedExampleObjectFactory);

    example1 = {
      question: {
        html: 'worked example question 1',
        content_id: 'worked_example_q_1'
      },
      explanation: {
        html: 'worked example explanation 1',
        content_id: 'worked_example_e_1'
      }
    };
    example2 = {
      question: {
        html: 'worked example question 2',
        content_id: 'worked_example_q_2'
      },
      explanation: {
        html: 'worked example explanation 2',
        content_id: 'worked_example_e_2'
      }
    };
    conceptCardDict = {
      explanation: {
        html: 'test explanation',
        content_id: 'explanation',
      },
      worked_examples: [example1, example2],
      recorded_voiceovers: {
        voiceovers_mapping: {
          explanation: {},
          worked_example_q_1: {
            q1: {
              filename: 'filename1.mp3',
              file_size_bytes: 100000,
              needs_update: false,
              duration_secs: 10.0
            }
          },
          worked_example_e_1: {},
          worked_example_q_2: {},
          worked_example_e_2: {}
        }
      }
    };
  });

  it('should create a new concept card from a backend dictionary', () => {
    let conceptCard =
          conceptCardObjectFactory.createFromBackendDict(conceptCardDict);
    expect(conceptCard.getExplanation()).toEqual(
      SubtitledHtml.createDefault(
        'test explanation', 'explanation'));
    expect(conceptCard.getWorkedExamples()).toEqual([
      workedExampleObjectFactory.create(
        SubtitledHtml.createDefault(
          'worked example question 1', 'worked_example_q_1'),
        SubtitledHtml.createDefault(
          'worked example explanation 1', 'worked_example_e_1')),
      workedExampleObjectFactory.create(
        SubtitledHtml.createDefault(
          'worked example question 2', 'worked_example_q_2'),
        SubtitledHtml.createDefault(
          'worked example explanation 2', 'worked_example_e_2'))
    ]);
  });

  it('should convert to a backend dictionary', () => {
    let conceptCard =
        conceptCardObjectFactory.createFromBackendDict(conceptCardDict);
    expect(conceptCard.toBackendDict()).toEqual(conceptCardDict);
  });

  it('should create an interstitial concept card', () => {
    let conceptCard =
        conceptCardObjectFactory.createInterstitialConceptCard();
    expect(conceptCard.getExplanation()).toEqual(
      SubtitledHtml.createDefault(
        'Loading review material', 'explanation'));
    expect(conceptCard.getWorkedExamples()).toEqual([]);
  });

  it('should return recorded voice overs when called', () => {
    let voiceover = {
      voiceovers_mapping: {
        content: {
          en: {
            filename: 'filename1.mp3',
            file_size_bytes: 100000,
            needs_update: false,
            duration_secs: 10.0
          },
          hi: {
            filename: 'filename2.mp3',
            file_size_bytes: 11000,
            needs_update: false,
            duration_secs: 0.11
          }
        }
      }
    };

    conceptCardDict.recorded_voiceovers = voiceover;
    let conceptCard =
          conceptCardObjectFactory.createFromBackendDict(conceptCardDict);

    expect(conceptCard.getRecordedVoiceovers())
      .toEqual(RecordedVoiceovers.createFromBackendDict(voiceover));
  });
});
