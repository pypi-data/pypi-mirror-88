// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains a merging, transforming, and then filtering workflow
*/

import { 
    addColumnButton,
    columnHeaderChangeErrorSelector,
    columnHeaderChangeInputSelector,
    getCellSelector,
    getColumnHeaderContainerSelector,
    getColumnHeaderNameSelector,
    getTabSelector,
    mergeButton,
    modalAdvanceButtonSelector,
    modalHeaderSelector,
    modalSelector,
} from './utils/selectors';

import { 
    applyFiltersToColumn,
    checkColumn,
    checkGeneratedCode,
    createNotebookRunCell,
    deleteAllNotebooks,
    setFormula,
    sortColumn
} from './utils/helpers';
import { Selector } from 'testcafe';


fixture `Test Merge Transform Filter Workflow`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'first_name\': [\'Nate\', \'Aaron\', \'Jake\']})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'last_name\': [\'rush\', \'Diamond-Reivich\', \'diamond-reivich\']})\nmitosheet.sheet(df1, df2)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Merge Transform Filter', async t => {
    // Do the merge
    await t
        .click(mergeButton)
        .expect(modalSelector.exists).ok()
        .expect(modalHeaderSelector.innerText).contains('Merge')
        .expect(modalAdvanceButtonSelector.innerText).eql('Merge')
        .click(modalAdvanceButtonSelector)

    // Make sure the new sheet has been created correctly & switch sheets
    await t
        .click(getTabSelector('df3'))
    
    // Create a new column
    await t.click(addColumnButton)

    // Open column rename model
    await t
        .click(getColumnHeaderNameSelector('D'))
        .expect(modalSelector.exists).ok()
        .expect(modalHeaderSelector.innerText).contains('Change Column Name: D')
        .expect(modalAdvanceButtonSelector.innerText).eql('Change Column Name')

    // Change column name to full_name
    await t
        .typeText(columnHeaderChangeInputSelector, "full_name")
        .expect(columnHeaderChangeErrorSelector.exists).notOk()
        .click(modalAdvanceButtonSelector)
        .expect(getColumnHeaderContainerSelector('full_name').exists).ok()

    // Set column formula to concat first name and last name
    await setFormula(t, '=CONCAT(first_name, " ", last_name)', 'full_name', '0');

    // then update the last_name column to upper case 
    await setFormula(t, '=UPPER(CONCAT(first_name, " ", last_name))', 'full_name', '0');

    // only keep rows whose full name column contains 'VICH'
    await applyFiltersToColumn(
        t, 
        'full_name', 
        [
            {filterCondition: 'contains', filterValue: 'VICH'},
        ]
    )
    await checkColumn(t, 'full_name', ['AARON DIAMOND-REIVICH', 'JAKE DIAMOND-REIVICH']);

    const expectedDf = {
        'id': ['2', '3'],
        'first_name': ['AARON', 'JAKE'],
        'last_name': ['DIAMOND-REIVICH', 'DIAMOND-REIVICH'],
        'full_name': ['AARON DIAMOND-REIVICH', 'JAKE DIAMOND-REIVICH']
    }

    checkGeneratedCode(t, 'df3', expectedDf)
});

