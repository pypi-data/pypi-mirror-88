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
    checkGeneratedCode,
    checkSheet,
    createNotebookRunCell,
    deleteAllNotebooks,
    DELETE_PRESS_KEYS_STRING,
    doGroup,
    setFormula,
} from './utils/helpers';


fixture `Test Group`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await createNotebookRunCell(t, "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'gender': ['male','male','female', 'female', 'female'], 'species': ['human','dog','human', 'human', 'dog'], 'size': ['big', 'small', 'small', 'big', 'big'],'weight': [160, 20, 110, 175, 95]})\nmitosheet.sheet(df1)");
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Allows for a basic group with a single row', async t => {
    await doGroup(t, ['gender'], [], [{columnHeader: 'weight', aggfunc: 'sum'}])
    await t.click(getTabSelector('df2'))

    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    })

});


test('Allows for a mulitple group with a single row', async t => {
    await doGroup(t, ['gender'], [], [{columnHeader: 'weight', aggfunc: 'sum'}])
    await doGroup(t, ['gender'], [], [{columnHeader: 'weight', aggfunc: 'sum'}])
    
    await t.click(getTabSelector('df2'))

    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    })

    await t.click(getTabSelector('df3'))
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    })


});


test('Grouping with mulitple rows and a column', async t => {
    await doGroup(t, ['gender', 'species'], ['size'], [{columnHeader: 'weight', aggfunc: 'sum'}])

    await t.click(getTabSelector('df2'))

    await checkSheet(t, {
        'gender': ['female', 'female', 'male', 'male'],
        'species': ['dog', 'human', 'dog', 'human'],
        'weight_big': ['95', '175', 'NaN', '160'],
        'weight_small': ['NaN', '110', '20', 'NaN'],
    })

    // note: we need to have a different expected sheet for checking the generated
    // code because the values in a column with NaN gets formatted as a float
    const expectedSheet = {
        'gender': ['female', 'female', 'male', 'male'],
        'species': ['dog', 'human', 'dog', 'human'],
        'weight_big': ['95.0', '175.0', 'NaN', '160.0'],
        'weight_small': ['NaN', '110.0', '20.0', 'NaN'],
    }

    await checkGeneratedCode(t, 'df2', expectedSheet)
});