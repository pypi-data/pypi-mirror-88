// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import { 
    getTabSelector,
    getCellSelector,
    mergeButton,
    modalSelector,
    modalHeaderSelector,
    modalAdvanceButtonSelector,
    addColumnButton,
} from './utils/selectors';

import { 
    createNotebookRunCell,
    deleteAllNotebooks,
    setFormula,
} from './utils/helpers';


fixture `Test Merge Functionality`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [101, 102, 103]})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [201, 202, 203]})\nmitosheet.sheet(df1, df2)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Merge opens modal, detects shared keys, creates new dataframe', async t => {
    // Do the merge
    await t
        .click(mergeButton)
        .expect(modalSelector.exists).ok()
        .expect(modalHeaderSelector.innerText).contains('Merge')
        .expect(modalAdvanceButtonSelector.innerText).eql('Merge')
        .click(modalAdvanceButtonSelector)

    // Make sure the new sheet has been created correctly.
    await t
        .expect(getTabSelector('df3').exists).ok()
        .click(getTabSelector('df3'))
        .expect(getCellSelector('values_df1', '0').innerText).eql('101')
        .expect(getCellSelector('values_df2', '0').innerText).eql('201')

    // Make sure we can add a column to the new sheet
    await t.click(addColumnButton)
    await setFormula(t, '=values_df1 + values_df2', 'D', '0')
    await t.expect(getCellSelector('D', '0').innerText).eql('302')

    // Do another merge merge
    await t
        .click(mergeButton)
        .expect(modalSelector.exists).ok()
        .expect(modalHeaderSelector.innerText).contains('Merge')
        .expect(modalAdvanceButtonSelector.innerText).eql('Merge')
        .click(modalAdvanceButtonSelector)

    // Again, make sure the new tab is created
    await t
        .expect(getTabSelector('df4').exists).ok()
        .click(getTabSelector('df4'))
        .expect(getCellSelector('values_df1', '0').innerText).eql('101')
        .expect(getCellSelector('values_df2', '0').innerText).eql('201')
});
   
   