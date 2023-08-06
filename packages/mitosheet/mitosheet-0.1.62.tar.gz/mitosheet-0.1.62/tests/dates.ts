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


fixture `Test Handles Dates`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'name': ['alice','bob','charlie'], 'dob': ['2005-10-23','2002-10-2','2001-11-14']})\ndf1['dob'] = pd.to_datetime(df1['dob'])\nmitosheet.sheet(df1)");
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Test displays dates, works with date functions', async t => {
    await checkColumn(t, 'dob', ['2005-10-23 00:00:00', '2002-10-02 00:00:00', '2001-11-14 00:00:00'])

    await t.click(addColumnButton);
    await setFormula(t, '=DAY(dob)', 'C', '0');

    await t.click(addColumnButton);
    await setFormula(t, '=MONTH(dob)', 'D', '0');

    await t.click(addColumnButton);
    await setFormula(t, '=YEAR(dob)', 'E', '0');

    await t.click(addColumnButton);
    await setFormula(t, '=DATEVALUE(CONCAT(E, \'-\', D, \'-\', C))', 'F', '0');
    await checkColumn(t, 'F', ['2005-10-23 00:00:00', '2002-10-02 00:00:00', '2001-11-14 00:00:00'])

});