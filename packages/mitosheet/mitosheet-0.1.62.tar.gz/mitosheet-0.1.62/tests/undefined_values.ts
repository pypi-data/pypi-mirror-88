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
} from './utils/helpers';


fixture `Test Handles Undefined Values`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'Name': ['Nate', 'Aaron', None], 'Height': ['4', None, 7], 'Weight': [None, 300, 400]})\nmitosheet.sheet(df1)");
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Test displays NaNs', async t => {
    await checkColumn(t, 'Name', ['Nate', 'Aaron', 'NaN'])
    await checkColumn(t, 'Height', ['4', 'NaN', '7'])
    await checkColumn(t, 'Weight', ['NaN', '300', '400'])
});

// See here: https://devexpress.github.io/testcafe/documentation/recipes/basics/test-select-elements.html
test('Test allows you to divide NaNs, only carries through in rows', async t => {
    await t.click(addColumnButton);
    await setFormula(t, '=Height/Weight', 'D', '0');
    await checkColumn(t, 'D', ['NaN', 'NaN', '0.0175'])
});

test('Test allows you to filter out NaNs', async t => {
    await t.click(addColumnButton);
    await setFormula(t, '=Height/Weight', 'D', '0');

    await applyFiltersToColumn(
        t, 
        'D', 
        [
            {filterCondition: 'is not empty', filterValue: undefined},
        ],
    )
    await checkColumn(t, 'D', ['0.0175'])
});
