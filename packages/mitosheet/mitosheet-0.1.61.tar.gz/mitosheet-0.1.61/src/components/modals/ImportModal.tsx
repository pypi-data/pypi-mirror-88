// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useEffect, Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';

// import css
import "../../../css/all-modals.css"
import "../../../css/import-modal.css"
import { MitoAPI } from '../../api';

export enum ImportEnum {
    SimpleImport = 'simple_import',
    RawPythonImport = 'raw_python_import',
}

export const getDfNameError = (pythonCode: string, newDfNames: string[], existingDfNames: string[]): string | undefined => {
    for (let i = 0; i < newDfNames.length; i++) {
        // Invalid if it's not in the Python
        if (!pythonCode.includes(newDfNames[i])) {
            return `Error: ${newDfNames[i]} is not a name of a variable in your code.`;
        }
        // Or if it's already the name of a sheet
        if (existingDfNames.indexOf(newDfNames[i]) !== -1) {
            return `Error: ${newDfNames[i]} is already the name of a sheet. Please choose a different name.`;
        }
    }
    return undefined;
}


type ImportModalProps = {
    setModal: (modalInfo: ModalInfo) => void;
    send: (msg: Record<string, unknown>) => void,
    dfNames: string[];
    api: MitoAPI;
};

/* 
  A modal that allows a user to import data into the sheet.
*/
const ImportModal = (props: ImportModalProps): JSX.Element => {
    const [importType, setImportType] = useState<ImportEnum>(ImportEnum.SimpleImport);

    // Params for a simple import
    const [fileNames, setFileNames] = useState<string[]>([]);
    const [importedFiles, setImportedFiles] = useState<string[]>([]);

    // Params for a raw Python import
    const [pythonCode, setPythonCode] = useState<string>('');
    const [dfNamesString, setDfNamesString] = useState<string>('');
    const [dfNameError, setDfNameError] = useState<string>('');

    async function getDataFiles() {
        const dataFiles = await props.api.getDataFiles();
        setFileNames(dataFiles);
    }

    useEffect(() => {
        // To see an explination, read here: https://medium.com/better-programming/how-to-fetch-data-from-an-api-with-react-hooks-9e7202b8afcd
        // TL;DR: we load the data after the component renders
        getDataFiles();
    }, []) // empty array is necessary to have this run only once

    const updateImportedFile = (event: React.ChangeEvent<HTMLSelectElement>, index: number): void => {
        const newImports = [...importedFiles]
        newImports[index] = event.target.value;
        setImportedFiles(newImports)
    }

    const addNewFileImport = (): void => {
        const newImports = [...importedFiles];
        newImports.push(fileNames[0])
        setImportedFiles(newImports)
    }

    /*
        Completes the import step, casing on which sort of import is occuring
    */
    const clickImport = () => {
        if (importType === ImportEnum.SimpleImport) {
            window.logger?.track({
                userId: window.user_id,
                event: 'button_simple_import_log_event',
                properties: {
                    file_names: importedFiles
                }
            })
    
            props.send({
                'event': 'edit_event',
                'type': 'simple_import_edit',
                'file_names': importedFiles,
            })
    
            props.setModal({type: ModalEnum.None});
        } else {
            // Short curcit early if the user provides an invalid name
            const dfNames = dfNamesString.split(',').map(dfName => dfName.trim());
            const dfNameError = getDfNameError(pythonCode, dfNames, props.dfNames);
            if (dfNameError !== undefined) {
                return setDfNameError(dfNameError);
            }

            window.logger?.track({
                userId: window.user_id,
                event: 'button_raw_python_import_log_event',
                properties: {
                    'python_code': pythonCode,
                    'new_df_names': dfNames,
                }
            })
    
            props.send({
                'event': 'edit_event',
                'type': 'raw_python_import_edit',
                'python_code': pythonCode,
                'new_df_names': dfNames,
            })
    
            props.setModal({type: ModalEnum.None});
        }
    };

    return (
        <DefaultModal
        header={`Import Data`}
        modalType={ModalEnum.ReplayAnalysis}
        viewComponent= {
            <Fragment>
                <div className='modal-element-label'>
                    Import Method
                </div>
                <select className='merge-modal-sheet-dropdown' onChange={(e) => {setImportType(e.target.value as ImportEnum)}}>
                    <option key={ImportEnum.SimpleImport} value={ImportEnum.SimpleImport} selected={importType === ImportEnum.SimpleImport}> Simple Import</option>;
                    <option key={ImportEnum.RawPythonImport} value={ImportEnum.RawPythonImport} selected={importType === ImportEnum.RawPythonImport}> Raw Python Import</option>;
                </select>

                {importType === ImportEnum.SimpleImport &&
                    <div>
                        <div className='modal-element-label mt-2'>
                            Files to Import
                        </div>
                        {importedFiles.map((selectedFileName, importIndex) => {
                            return (<select key={importIndex} className='merge-modal-sheet-dropdown mb-1' onChange={(e) => updateImportedFile(e, importIndex)}>
                                {fileNames.map((fileName) => {
                                    return (<option key={fileName} value={fileName} selected={importedFiles[importIndex] === fileName}>{fileName}</option>);
                                })}
                            </select>)
                        })}
                        <div className='modal-add' onClick={addNewFileImport}>
                            + Add File
                        </div>
                        

                    </div>
                }
                {importType === ImportEnum.RawPythonImport &&
                    <div>
                        <div className='modal-element-label mt-2'>
                            Python Code
                        </div>
                        <textarea 
                            className='raw-python-textarea'
                            rows={5} 
                            value={pythonCode} 
                            onChange={(e) => {setPythonCode(e.target.value)}}
                            autoFocus />
                        <div className='modal-element-label mt-2'>
                            Dataframe Variable Names to Import (comma seperated)
                        </div>
                        <input 
                            className="modal-input"
                            type="text" 
                            placeholder='df1, df2' 
                            value={dfNamesString} 
                            onChange={(e) => {setDfNamesString(e.target.value)}} />
                        {dfNameError !== '' && 
                            <div className='modal-error'>
                                {dfNameError}
                            </div>
                        }
                    </div>
                    
                }


            </Fragment>
        }
        buttons = {
            <Fragment>
                <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                <div className='modal-action-button modal-dual-button-right' onClick={clickImport}> Import </div>
            </Fragment>
        }
    />
    )
} 

export default ImportModal;