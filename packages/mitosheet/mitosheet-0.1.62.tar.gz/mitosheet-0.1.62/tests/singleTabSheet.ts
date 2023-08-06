// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    addColumnButton,
    documentationButton,
    documentationSidebarSelector,
    getCellSelector,
} from './utils/selectors';

import { 
    checkColumn,
    createNotebookRunCell,
    deleteAllNotebooks,
    setFormula
} from './utils/helpers';



fixture `Create a Single Tab Mitosheet`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={\'A\': [1, 2, 3], \'B\': [\'Aaron Diamond-Reivich\', \'Nate Rush\', \'Jake Diamond-Reivich\']})\nmitosheet.sheet(df)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('can open and see documentation', async t => {
    await t
        .click(documentationButton)
        .expect(documentationSidebarSelector.exists).ok()
});


test('added column can have set formula', async t => {
    await t.click(addColumnButton)
    await setFormula(t, '=77', 'C', '0')
    await t.expect(getCellSelector('C', '0').innerText).eql('77')
    await setFormula(t, '=77 * 2', 'C', '0')
    await t.expect(getCellSelector('C', '0').innerText).eql('154')
});
   

test('column updates propagate through', async t => {
    // Update three columns (wait a little inbetween for them to update)
    await t.click(addColumnButton)
    await setFormula(t, '=A', 'C', '0')

    await t.click(addColumnButton)
    await setFormula(t, '=C', 'D', '0')

    await t.click(addColumnButton)
    await setFormula(t, '=D', 'E', '0')

    // Check the final value, update, and then check the value again
    await t.expect(getCellSelector('E', '0').innerText).eql('1')
    await setFormula(t, '=A + 1', 'C', '0')
    await t.expect(getCellSelector('E', '0').innerText).eql('2')
});

test('string clean workflow', async t => {
    // Get the first name in column C
    await t.click(addColumnButton)
    await setFormula(t, '=LEFT(B, FIND(B, " ") - 1)', 'C', '0')

    // Get the last initial in column D
    await t.click(addColumnButton)
    await setFormula(t, '=MID(B, FIND(B, " ") + 1, 1)', 'D', '0')

    await checkColumn(t, 'C', ['Aaron', 'Nate', 'Jake']);
    await checkColumn(t, 'D', ['D', 'R', 'D']);

    // Concat them together, and check the result
    await t.click(addColumnButton)
    await setFormula(t, '=CONCAT(C, " ", D, ".")', 'E', '0')
    await checkColumn(t, 'E', ['Aaron D.', 'Nate R.', 'Jake D.']);

});


test('If statements functions', async t => {
    await t.click(addColumnButton)
    await setFormula(t, '=IF(A > 1, 1, 0)', 'C', '0')
    await checkColumn(t, 'C', ['0', '1', '1']);

    await setFormula(t, '=IF(AND(A > 1, A < 3), 1, 0)', 'C', '0')
    await checkColumn(t, 'C', ['0', '1', '0']);

    await setFormula(t, '=IF(OR(A > 1, A < 3), 1, 0)', 'C', '0')
    await checkColumn(t, 'C', ['1', '1', '1']);
});
