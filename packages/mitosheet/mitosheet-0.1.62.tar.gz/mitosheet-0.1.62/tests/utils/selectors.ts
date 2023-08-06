// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all the selectors used across Mito frontend tests. 
*/

import { Selector} from 'testcafe';

// PURE JUPYTER SELECTORS

export const mainPanel = Selector('#jp-main-content-panel')

export const fileTab = Selector('#jp-MainMenu')
    .child('ul')
    .child('li')
    .child('div')
    .withText('File');

export const fileTabNew = Selector('div.lm-Menu-itemLabel')
    .withText('New');

export const fileTabCloseAllTabs = Selector('div.lm-Menu-itemLabel')
    .withText('New');

export const fileTabNewNotebook = Selector('div.lm-Menu-itemLabel')
    .withExactText('Notebook');

export const selectKernelButton = Selector('div.jp-Dialog-buttonLabel')
    .withExactText('Select');

export const selectGeneratedCode = Selector('span.cm-comment')
    .withExactText('# MITO CODE START (DO NOT EDIT)');

export const selectLastLineOfGeneratedCode = Selector('span.cm-comment')
    .withExactText('# MITO CODE END (DO NOT EDIT)');

export const printedOutput = Selector('div.jp-OutputArea-output').child('pre')

// MITO SELECTORS

export const mito = Selector('div.mitosheet');

export const mitoToolbarContainerLeft = Selector('div.mito-toolbar-container-left')


// TODO: this does not need to be a function
export const getFormulaBarSelector = (): Selector => {
    return Selector('button.formula-bar-input');
}

// MITO TOOLBAR BUTTONS (NOTE: note all of these have been tested)


export const addColumnButton = Selector('div')
    .withExactText('Add Column')
    .parent()

export const deleteColumnButton = Selector('div')
    .withExactText('Delete Column')
    .parent()

export const groupButton = Selector('div')
    .withExactText('Group')
    .parent()

export const mergeButton = Selector('div')
    .withExactText('Merge')
    .parent()

export const saveButton = Selector('div')
    .withExactText('Save')
    .parent()

export const repeatAnalysisButton = Selector('div')
    .withExactText('Repeat Saved Analysis')
    .parent()

export const downloadSheetButton = Selector('div')
    .withExactText('Download Sheet')
    .parent()

export const documentationButton = Selector('div.tooltip')
    .withExactText('Documentation')
    .parent()

// DOCUMENTATION INTERACTION SELECTORS

export const documentationSidebarSelector = Selector('div.documentation-sidebar-container')


// MODAL INTERACTION SELECTORS

export const modalSelector = Selector('div.modal')
export const modalHeaderSelector = Selector('div.modal-header-text-div')
export const modalInput = Selector('input.modal-input')
export const modalCloseButtonSelector = Selector('div.modal-dual-button-left')
export const modalAdvanceButtonSelector = Selector('div.modal-dual-button-right')

/* 
    Helper function that returns a selector for the given
    columnHeader container - which is the entire box for the column header
    (includes the name and the filter).
*/
export const getColumnHeaderContainerSelector = (columnHeader: string): Selector => {    
    return Selector('div.ag-header-cell')
        .withAttribute('col-id', columnHeader)
}

/* 
    Helper function that returns a selector for the given
    columnHeader - but just the name (what you click to change)
    the name.
*/
export const getColumnHeaderNameSelector = (columnHeader: string): Selector => {    
    return Selector('div.column-header-column-header')
        .withExactText(columnHeader);
}


export const getColumnHeaderFilterSelector = (columnHeader: string): Selector => {
    return getColumnHeaderContainerSelector(columnHeader)
        .find('div.column-header-filter-button')
}

/* 
    Helper function that returns a selector for the cell at columnHeader, row
*/
export const getCellSelector = (columnHeader: string, row: string): Selector => {    
    return Selector('div.ag-row')
        .withAttribute('row-index', row)
        .child('div')
        .withAttribute('col-id', columnHeader)
}

/* 
    Helper function that returns a selector for a tab with the passed
    tab name.
*/
export const getTabSelector = (tabName: string): Selector => {    
    return Selector('p.tab-sheet-name')
        .withExactText(tabName)
        .parent()
        .parent()
        .parent()
}

// CHANGE COLUMN HEADER MODAL
export const columnHeaderChangeInputSelector = Selector('input.column-header-input');
export const columnHeaderChangeErrorSelector = Selector('p.column-header-error');

// ERROR MODAL
export const errorMessageSelector = Selector('div.modal-message')
    .child('div')
    .nth(0)

// REPEAT ANALYSIS MODAL
/* 
    Helper function that returns a selector for a saved analysis in the
    saved analysis list
*/
export const getSavedAnalysisItem = (savedAnalysisName: string): Selector => {    
    return Selector('input')
        .withAttribute('name', savedAnalysisName)
}

// FILTER MODAL
export const addFilterButton = Selector('div.filter-modal-add-value');
export const filterConditionSelector = Selector('select.filter-modal-condition-select')
export const filterConditionOptionSelector = filterConditionSelector
    .find('option')
export const filterValueInputSelector = Selector('input.filter-modal-value-input')
export const operatorSelector = Selector('select.filter-modal-input')
    .nth(1) // We always take the second, because the first is invisible
export const operatorOptionSelector = operatorSelector
    .find('option')


// GROUP MODAL
export const rowContainerSelector = Selector('div.group-modal-column-selection')
    .nth(0)
    .find('input')
export const columnContainerSelector = Selector('div.group-modal-column-selection')
    .nth(1)
    .find('input')
export const deleteAggregationSelector = Selector('rect').withAttribute('width', '13');
export const groupModalAddValueSelector = Selector('div.group-modal-add-value');
export const valueMappingKey = Selector('select.group-modal-value-mapping-key');
export const valueMappingKeyOptions = Selector('select.group-modal-value-mapping-key')
    .find('option')
export const valueMappingValue = Selector('select.group-modal-value-mapping-value');
export const valueMappingValueOptions = Selector('select.group-modal-value-mapping-value')
    .find('option')

// SORT MODAL
export const ascendingSortSelector = Selector('button.sort-button').withText('Ascending')
export const descendingSortSelector = Selector('button.sort-button').withText('Descending')



// MISC SELECTORS

export const getActiveElement = Selector(() => {
    return document.activeElement
});