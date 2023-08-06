// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';


// import css
import "../../../css/replay-analysis-modal.css"
import { MitoAPI } from '../../api';

type ReplayAnalysisProps = {
    setModal: (modalInfo: ModalInfo) => void;
    send: (msg: Record<string, unknown>) => void,
    savedAnalysisNames: string[];
    api: MitoAPI
};


/* 
    A modal that displays the all existing, saved analyses, and lets
    a user select an analysis to rerun.
*/
const ReplayAnalysis = (props: ReplayAnalysisProps): JSX.Element => {
    const [selectedAnalysisIndex, setSelectedAnalysisIndex] = useState(-1);

    const replayAnalysis = async () => {
        const analysisName = props.savedAnalysisNames[selectedAnalysisIndex];

        // First, we check if there are any simple import steps that we need to handle with special
        // care, specifically by asking the users to switch out the files for new files.
        const importSummary = await props.api.getImportSummary(analysisName);
        if (Object.keys(importSummary).length !== 0) {
            props.setModal({type: ModalEnum.ReplayImport, analysisName: analysisName, importSummary: importSummary});
            return;
        }


        window.logger?.track({
            userId: window.user_id,
            event: 'button_replay_analysis_log_event',
            properties: {
                stage: 'repeated',
                analysis_name: analysisName
            }
        })

        props.send({
            'event': 'update_event',
            'type': 'use_existing_analysis_update',
            'analysis_name': analysisName
        });

        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
        header={`Rerun an existing analysis on current data`}
        modalType={ModalEnum.ReplayAnalysis}
        viewComponent= {
            <Fragment>
                <div className='mt-2 replay-analysis-analysis-selection-container'>
                    <div className='replay-analysis-label'>
                        Select an existing analysis
                    </div>
                    <div className='replay-analysis-analysis-selection'>
                        {props.savedAnalysisNames.length == 0 &&
                            <p>
                                Save an analysis to have it appear here.
                            </p>
                        }
                        {props.savedAnalysisNames.map((savedAnalysisName, index) => {
                            const isSelected = selectedAnalysisIndex === index;
                            return (
                            <div key={savedAnalysisName}>
                                <input
                                    key={savedAnalysisName}
                                    type="checkbox"
                                    name={savedAnalysisName}
                                    checked={isSelected}
                                    onChange={() => {setSelectedAnalysisIndex(index);}}
                                />
                                {savedAnalysisName}
                            </div>
                            )
                        })}
                    </div>
                </div>                
            </Fragment>
        }
        buttons = {
            <Fragment>
                <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                <div className='modal-action-button modal-dual-button-right' onClick={replayAnalysis}> {"Replay"}</div>
            </Fragment>
        }
    />
    )
} 

export default ReplayAnalysis;