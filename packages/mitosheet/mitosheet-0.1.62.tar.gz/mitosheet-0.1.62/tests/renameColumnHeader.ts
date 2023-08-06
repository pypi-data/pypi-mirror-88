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
} from './utils/selectors';

import { 
    createNotebookRunCell,
    deleteAllNotebooks,
    setFormula,
    DELETE_PRESS_KEYS_STRING
} from './utils/helpers';


fixture `Test Rename Column Headers`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [101, 102, 103]})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [201, 202, 203]})\nmitosheet.sheet(df1, df2)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Allows you to rename to valid headers only', async t => {
    
    await t
        .click(getColumnHeaderNameSelector('id'))
        .expect(modalSelector.exists).ok()
        .expect(modalHeaderSelector.innerText).contains('Change Column Name: id')
        .expect(modalAdvanceButtonSelector.innerText).eql('Change Column Name')

    // Enter some invalid headers, and get error messages
    await t
        .typeText(columnHeaderChangeInputSelector, "123")
        .expect(columnHeaderChangeErrorSelector.exists).ok()
        .pressKey(DELETE_PRESS_KEYS_STRING)
        .typeText(columnHeaderChangeInputSelector, "h a")
        .expect(columnHeaderChangeErrorSelector.exists).ok()
        .pressKey(DELETE_PRESS_KEYS_STRING)
        .typeText(columnHeaderChangeInputSelector, "h-a")
        .expect(columnHeaderChangeErrorSelector.exists).ok()
        .pressKey(DELETE_PRESS_KEYS_STRING)
    
    // Finially, change to a valid header, and make sure the change goes through
    await t
        .typeText(columnHeaderChangeInputSelector, "h_a")
        .expect(columnHeaderChangeErrorSelector.exists).notOk()
        .click(modalAdvanceButtonSelector)
        .expect(getColumnHeaderContainerSelector('h_a').exists).ok()
});
   