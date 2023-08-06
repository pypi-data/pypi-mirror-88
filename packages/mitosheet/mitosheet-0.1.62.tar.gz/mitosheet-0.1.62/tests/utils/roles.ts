// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all roles, which are the predefined ways of logging into
    the mito testing infrastructure.
*/

import { Role } from 'testcafe';

export const testUser = Role('http://staging.trymito.io', async t => {
    await t
        .typeText('#username_input', 'test')
        .typeText('#password_input', 'test')
        .click('#login_submit')
});