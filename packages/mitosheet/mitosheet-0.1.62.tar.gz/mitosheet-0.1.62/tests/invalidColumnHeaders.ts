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
    checkSheet,
    createNotebookRunCell,
    deleteAllNotebooks,
    DELETE_PRESS_KEYS_STRING,
    setFormula,
    sortColumn,
} from './utils/helpers';


fixture `Test Invalid Column Headers`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'What is your first name?': ['Nate'], 'What is your height?!': [4], 'Weight-Of-You': [100]})\nmitosheet.sheet(df1)");
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Displays sheet', async t => {
    await checkSheet(t, {
        'What_is_your_first_name_': ['Nate'],
        'What_is_your_height__': ['4'],
        'Weight_Of_You': ['100']
    })
});