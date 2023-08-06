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
    repeatAnalysisButton,
    modalInput,
    saveButton,
    getSavedAnalysisItem,
} from './utils/selectors';

import { 
    createNotebookRunCell,
    deleteAllNotebooks,
    setFormula,
} from './utils/helpers';


fixture `Test Save and Repeat`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\nmitosheet.sheet(df1)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

// Generate a random ID to save the test
const randomId = '_' + Math.random().toString(36).substr(2, 9);

test('Save analysis saves, repeat analysis repeats', async t => {
    await t
        .click(addColumnButton)
        .click(saveButton)
        .typeText(modalInput, randomId)
        .click(modalAdvanceButtonSelector) // actually save it
    
    // Delete all notebooks
    await deleteAllNotebooks(t)

    // Create a new blank notebook
    await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\nmitosheet.sheet(df1)');

    // Repeat the analysis on this new blank notebook
    await t
        .click(repeatAnalysisButton)
        .click(getSavedAnalysisItem(randomId))
        .click(modalAdvanceButtonSelector)
        .expect(getColumnHeaderContainerSelector('B').exists).ok()
});
   