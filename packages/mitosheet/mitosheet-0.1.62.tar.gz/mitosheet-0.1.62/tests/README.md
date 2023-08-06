# Running Frontend Tests

See the main `README.md` for instructions on running the tests!

# Getting Started Writing Testcafe Tests

To start writing tests, see the tests in `singleTabSheet.ts`. This file contains three sections worth highlighting:
1. A `beforeEach` function call, where we create the Mitosheet we want and render it. This runs at the start of _every test_ (note that it deletes all other notebooks to do this).
2. An `afterEach` function call, where we delete all existing notebooks (as they just cause problems by causing a select modal popup to appear).
3. The tests themselves. Note how the tests in this file use utilities written in the `utils.ts` file - do use these! 

Note, the testcafe documentation is pretty good - and you can see it [here](https://devexpress.github.io/testcafe/documentation/guides/).

# Writing Selectors

Writing selectors is hard, sometimes. It takes a bit to get the hang of it. For this reason, I've tried to write selectors for some common items - and you can just reuse them!

Also, write and write some of your own. It can be really challenging, but you will learn a lot. See the testcafe documentation [here](https://devexpress.github.io/testcafe/documentation/guides/basic-guides/select-page-elements.html).

# Common Gotchas

1. NOTE: when writing a new test, do `test.only(` to just run that single test. This will _dramatically_ speed up your development. 
2. _Make sure you write/debug tests in the browser you're running them in_. Not everything is the same everywhere, so keeping things static is absolutely essential.
3. Make sure to check out existing tests to see the easiest ways to write a formula, check a column header, and check the value of a cell. There are lot of useful utilities.
4. The tests are much more robust than reflect, but they sometimes fail. If you see a test fail randomly, see if you can figure out why and fix it, so we can keep making these tests more robust!