// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all the selectors used across Mito frontend tests. 
*/

import { Selector} from 'testcafe';
import { testUser } from './roles';
import { 
    getCellSelector, 
    selectKernelButton,
    fileTab,
    fileTabNew,
    fileTabNewNotebook,
    getActiveElement,
    getColumnHeaderFilterSelector,
    addFilterButton,
    filterConditionSelector,
    filterConditionOptionSelector,
    filterValueInputSelector,
    modalAdvanceButtonSelector,
    operatorSelector,
    operatorOptionSelector,
    groupButton,
    rowContainerSelector,
    columnContainerSelector,
    deleteAggregationSelector,
    groupModalAddValueSelector,
    valueMappingKey,
    valueMappingKeyOptions,
    valueMappingValue,
    valueMappingValueOptions,
    ascendingSortSelector,
    descendingSortSelector,
    selectGeneratedCode,
    selectLastLineOfGeneratedCode,
    printedOutput
} from './selectors';

// A string you can pass to t.pressKeys that will delete all values from the currently selecte input
export const DELETE_PRESS_KEYS_STRING = 'ctrl+a delete'


export type FilterType = {
    filterCondition: string,
    filterValue?: string 
}

/*
    Applies the given filters to a column. Notably, deletes all other filters that may be on 
    the column at that time to apply these filters!
*/
export async function applyFiltersToColumn(
        t: TestController, 
        columnHeader: string, 
        filters: FilterType[],
        operator?: 'Or' | 'And'
    ): Promise<void> {

    // Open the filter modal
    await t.click(getColumnHeaderFilterSelector(columnHeader))

    const filterTableSelector = Selector('div.filter-modal-centering-container')
        .find('table')

    const numFilters = await filterTableSelector.child('tr').count;

    // Delete all existing filters
    for (let i = 0; i < numFilters - 1; i++) {
        const deleteFilterSelector = Selector('rect').withAttribute('width', '13')
        await t.click(deleteFilterSelector)
    }

    for (let i = 0; i < filters.length; i++) {
        await t.click(addFilterButton)

        const filterCondition = filters[i].filterCondition;
        const filterValue = filters[i].filterValue;

        await t
            .click(filterConditionSelector.nth(i))
            .click(filterConditionOptionSelector.withExactText(filterCondition).nth(i))
            

        if (filterValue !== undefined) {
            await t
                .click(filterValueInputSelector.nth(i))
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(filterValueInputSelector.nth(i), filterValue)
        }
    }

    // If there is an operator, and it makes sense to apply it, we apply it
    if (operator !== undefined) {
        await t
            .click(operatorSelector)
            .click(operatorOptionSelector.withExactText(operator));
    }


    await t.click(modalAdvanceButtonSelector)
}


/*
    Sets a a formula at the given columnHeader, row to the correct value
*/
export async function setFormula(t: TestController, formula: string, columnHeader: string, row: string): Promise<void> {
    const cell = getCellSelector(columnHeader, row);

    await t
        .click(cell)
        .pressKey('enter')
        .selectText(Selector('input.ag-cell-inline-editing'))
        // NOTE: somehow, this deletes whatever formula is there, no matter how
        // long the formula is... I'll take it!
        .pressKey('delete+delete') 
        .typeText(Selector('input.ag-cell-inline-editing'), formula)
        .pressKey('enter')
}

/*
    Does a pivot with the passed params
*/
export async function doGroup(t: TestController, rows: string[], columns: string[], values: {columnHeader: string, aggfunc: string}[]): Promise<void> {
    
    // Open the group modal
    await t.click(groupButton)

    // Select rows
    for (let i = 0; i < rows.length; i++) {
        await t.click(rowContainerSelector.withAttribute('name', rows[i]));
    }

    // And the columns
    for (let i = 0; i < columns.length; i++) {
        await t.click(columnContainerSelector.withAttribute('name', columns[i]));
    }

    // Delete the existing aggregation value
    await t.click(deleteAggregationSelector);

    // And then add aggregation values placeholders
    for (let i = 0; i < values.length; i++) {
        await t.click(groupModalAddValueSelector);
    }

    // Finially, add the aggregation values
    for (let i = 0; i < values.length; i++) {
        const columnHeader = values[i].columnHeader
        const aggfunc = values[i].aggfunc;

        await t
            .click(valueMappingKey.nth(i))
            .click(valueMappingKeyOptions.withExactText(columnHeader).nth(i))
        await t
            .click(valueMappingValue.nth(i))
            .click(valueMappingValueOptions.withExactText(aggfunc).nth(i))
    }

    await t.click(modalAdvanceButtonSelector)
}

/*
    Sorts a column, yo.
*/
export async function sortColumn(t: TestController, columnHeader: string, direction: 'ascending' | 'descending'): Promise<void> {
    
    // Open the filter/sort modal
    await t.click(getColumnHeaderFilterSelector(columnHeader));

    if (direction === 'ascending') {
        await t.click(ascendingSortSelector);
    } else {
        await t.click(descendingSortSelector);
    }

    await t.click(modalAdvanceButtonSelector)
}


/*
    Helper function for checking that a given sheet has the passed data
*/
export async function checkSheet(t: TestController, dataFrame: Record<string, string[]>): Promise<void> {
    for (const key in dataFrame) {
        await checkColumn(t, key, dataFrame[key])
    }
}


/*
    Helper function for checking that a given printed datafame is expected
*/
/*
export async function(t: TestController, dataFrame: Record<string, string[]>): Promise<void> {
    for (const key in dataFrame) {
        const expectedOutput = '  String  Number        Date Mixed    E\n0    123     123  2001-01-01   123  123\n1      1       1  2002-01-01     1    1\n2      2       2  2003-01-01     2    2\n3      3       3  2004-01-01     3    3\n4      4       4  2005-01-01     4    4\n5      5       5  2006-01-01     5    5\n'

    }
}
*/


/*
    Helper function for checking that a given column has exactly columnValues inside
    of it, and nothing else. 
*/
export async function checkColumn(t: TestController, columnHeader: string, columnValues: string[]): Promise<void> {

    for (let i = 0; i < columnValues.length; i++) {
        // There is a warning generated by this line that is a testcafe bug fixed here: https://github.com/DevExpress/testcafe/issues/5389
        await t.expect(getCellSelector(columnHeader, i.toString()).innerText).eql(columnValues[i])
    }

    // And we check there are no other values
    await t.expect(getCellSelector(columnHeader, columnValues.length.toString()).exists).notOk();
}

export async function createNotebookRunCell(t: TestController, cellText: string): Promise<void> {
    // Creates a new notebook, and inserts the given cellText into that notebook

    // Log in 
    await t.useRole(testUser)

    // First, we check if there is currently a select kernel modal (which there is sometimes
    // when a notebook fails to be deleted, for some reason. If there is, we click it, as many
    // times as it pops up
    try {
        // Keep clicking kernel buttons, as long as they are there!
        while (!(await selectKernelButton.exists)) {
            await t.click(selectKernelButton)
        }
    } catch (e) {
        // We don't care if this fails... it only needs to happen it when does...
    }

    // Then, we delete all the notebooks there are
    await deleteAllNotebooks(t);


    await t
        // Then, we make a new notebook
        .click(fileTab)
        .hover(fileTabNew)
        .click(fileTabNewNotebook)

    // Then, we try to select a kernel (this popup only appears sometimes), 
    // which is why we don't necessarily _need_ to click it

    try {
        await t.click(selectKernelButton)
    } catch (e) {
        console.log("No need to select kernel.")
    }

    await t
        // Then, we create a mito notebook
        .typeText(
            // By default, the first cell is focused on
            getActiveElement(), 
            cellText
        )
        .pressKey('shift+enter')
}

export async function deleteAllNotebooks(t: TestController, failOnFailure?: boolean): Promise<void> {
    const notebookCount = await Selector('ul.jp-DirListing-content')
        .child('li')
        .count

    if (failOnFailure) {
        for (let i = 0; i < notebookCount; i++) {
            await deleteCurrentNotebook(t);
            // Wait for the UI to update, as to not crash shit.
            await t.wait(500);
        }
    } else {
        try {
            for (let i = 0; i < notebookCount; i++) {
                await deleteCurrentNotebook(t);
                // Wait for the UI to update, as to not crash shit.
                await t.wait(500);
            }
        } catch (e) {
            console.log('Failing deleting notebooks')
        }
    }    
}

export async function deleteCurrentNotebook(t: TestController): Promise<void> {
    const notebook = Selector('ul.jp-DirListing-content')
        .child('li')
        .nth(0)

    const deleteModalButton = Selector('div.jp-Dialog-buttonLabel')
        .withExactText('Delete')
    
    await t
        .rightClick(notebook)
        .pressKey('d')
        .click(deleteModalButton)
} 

export async function checkGeneratedCode(t: TestController, dfName: string, expectedDf: Record<string, string[]>): Promise<void> {
    
    // Select the Generated Code
    await t.click(selectGeneratedCode);

    // print out the edited df by:
    // 1. selecting the last line of the generated code
    await t.click(selectLastLineOfGeneratedCode);
    // 2. going to the end of the line
    let i = 0;
    for (i = 0; i < 16; i++) {
        await t.pressKey('right')
    } 

    // 3. create a new line
    await t.pressKey('enter')
    // 4. printing out the df
    await t.pressKey('p')
    await t.pressKey('r')
    await t.pressKey('i')
    await t.pressKey('n')
    await t.pressKey('t')
    await t.pressKey('(')

    // press the keys to type the dataframe name
    for (let i = 0; i < dfName.length; i++) {
        await t.pressKey(dfName.charAt(i))        
    }

    await t.pressKey(')')

    // run the cell
    await t.pressKey('shift+enter');

    /* converts string representation of df into js df 

        note: we convert from actual output to js df and not the other way
        because there seems to be a variable number of spaces between column headers, 
        which makes it hard to always properly format the string correctly. 
    
        -- IMPORTANT NOTE: this requires that no elements contain a space! --
    */

    const stringDf = printedOutput.innerText
    const rows = (await stringDf).split('\n');

    // add the index label
    rows[0] = 'index' + rows[0]
    const sheet = {}
    
    // fill in the column arrays with the values
    rows.forEach(row => {
        // condense any white spaces to a single ' ' 
        row = row.replace(/ +/g, ' ').trim()
        console.log(row)
        row.split(" ").forEach(function (element, index) {
            // if the sheet index does not exist, create it. This should only occur on the header row

            // make sure no blank strings ended up getting through 
            if (element === '') {
                return;
            }

            if (!sheet[index]) {
                sheet[index] = []
            }

            // add the element to the row
            sheet[index].push(element)
        });
    });

    // set the first array element for each object as the key
    Object.keys(sheet).forEach(key => {

        // rename the object key
        const newKey = sheet[key][0]
        Object.defineProperty(sheet, newKey,
            Object.getOwnPropertyDescriptor(sheet, key));

        // remove the old key
        delete sheet[key];

        // remove the first element from each value array
        sheet[newKey].shift()
    });

    // drop the index column
    delete sheet['index']

    // Then check that the actual df is what we expected!

    // first check that the column headers are the same
    await t.expect(Object.keys(sheet)).eql(Object.keys(expectedDf))

    // then check that the column values are the same
    for (let i = 0; i < Object.keys(sheet).length; i++) {
        Object.keys(sheet).forEach(async key => {
            await t.expect(sheet[key]).eql(expectedDf[key])
        });
    }
}

