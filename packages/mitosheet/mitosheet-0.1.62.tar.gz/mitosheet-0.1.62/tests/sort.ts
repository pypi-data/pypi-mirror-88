// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import { 
    getTabSelector,
    getCellSelector,
    modalSelector,
    modalHeaderSelector,
    modalAdvanceButtonSelector,
    addColumnButton,
    getColumnHeaderNameSelector,
    columnHeaderChangeInputSelector,
    columnHeaderChangeErrorSelector,
    getColumnHeaderContainerSelector,
    errorMessageSelector,
    modalCloseButtonSelector,
    getColumnHeaderFilterSelector,
    filterConditionSelector,
    filterConditionOptionSelector,
    filterValueInputSelector,
    addFilterButton,
} from './utils/selectors';

import { 
    applyFiltersToColumn,
    checkColumn,
    createNotebookRunCell,
    deleteAllNotebooks,
    DELETE_PRESS_KEYS_STRING,
    setFormula,
    sortColumn,
} from './utils/helpers';


fixture `Test Sorts`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'String': ['123', '1', '2', '3', '4', '5'], 'Number': [123, 1, 2, 3, 4, 5],'Date': ['2001-01-01', '2002-01-01', '2003-01-01','2004-01-01', '2005-01-01', '2006-01-01'],'Mixed': [123, '1', '2', '3', 4, 5]})\nmitosheet.sheet(df1)");
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Sort strings, numbers, dates ', async t => {
    await sortColumn(t, 'String', 'ascending');
    await checkColumn(t, 'String', ['1', '123', '2', '3', '4', '5'])
    await sortColumn(t, 'String', 'descending');
    await checkColumn(t, 'String', ['5', '4', '3', '2', '123', '1'])

    await sortColumn(t, 'Number', 'ascending');
    await checkColumn(t, 'String', ['1', '2', '3', '4', '5', '123'])
    await sortColumn(t, 'Number', 'descending');
    await checkColumn(t, 'String', ['123', '5', '4', '3', '2', '1'])

    await sortColumn(t, 'Date', 'ascending');
    await checkColumn(t, 'Date', ['2001-01-01', '2002-01-01', '2003-01-01', '2004-01-01', '2005-01-01', '2006-01-01'])
    await sortColumn(t, 'Date', 'descending');
    await checkColumn(t, 'Date', ['2006-01-01', '2005-01-01', '2004-01-01', '2003-01-01', '2002-01-01', '2001-01-01'])
});