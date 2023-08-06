// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.


/*
  Contains a wrapper around a strongly typed object that simulates a web-api. 
*/
// TODO: add a class that takes a _send_ and a _receive_, and then has functions for each call of the API


// Max delay is the longest we'll wait for the API to return a value
const MAX_DELAY = 5000;
// How often we poll to see if we have a response yet
const RETRY_DELAY = 250;
const MAX_RETRIES = MAX_DELAY / RETRY_DELAY;


const getRandomId = (): string => {
  return '_' + Math.random().toString(36).substr(2, 9);
}

// NOTE: these have pythonic field names because we parse their JSON directly in the API
export interface SimpleImportSummary {
  step_type: 'simple_import';
  file_names: string[];
}
export interface RawPythonImportSummary {
  step_type: 'raw_python_import';
  python_code: string;
  new_df_names: string[];
}

export interface ImportSummaries {
  [key: string]: SimpleImportSummary | RawPythonImportSummary
}

/*
  The MitoAPI class contains functions for interacting with the Mito backend.

  TODO: we should move _all_ calls to send inside of this class, and 
  wrap them inside of stronger-typed functions. 
*/
export class MitoAPI {
  send: (msg: Record<string, unknown>) => void;
  unconsumedResponses: Record<string, unknown>[];

  constructor(send: (msg: Record<string, unknown>) => void) {
    this.send = send;
    this.unconsumedResponses = [];
  }

  /*
    The receive response function is a workaround to the fact that we _do not_ have
    a real API in practice. If/when we do have a real API, we'll get rid of this function, 
    and allow the API to just make a call to a server, and wait on a response
  */
  receiveResponse(response: Record<string, unknown>): void {
    this.unconsumedResponses.push(response);
  }

  /*
    Helper function that tries to get the response for a given ID, and returns
    the data inside the 'data' key in this response if it exists. 

    Returns undefined if it does not get a response within the set timeframe
    for retries.
  */
  getResponseData(id: string): Promise<unknown | undefined> {
    
    return new Promise((resolve, reject) => {
      let tries = 0;
      const interval = setInterval(() => {
        // Only try at most MAX_RETRIES times
        tries++;
        if (tries > MAX_RETRIES) {
          clearInterval(interval);
          // If we fail, we return an empty response
          return resolve(undefined)
        }

        // See if there is an API response to this one specificially
        const index = this.unconsumedResponses.findIndex((response) => {
          return response['id'] === id;
        })
        if (index !== -1) {
          // Clear the interval
          clearInterval(interval);

          const response = this.unconsumedResponses[index];
          this.unconsumedResponses.splice(index, 1);
          
          return resolve(response['data']); // return to end execution
        } else {
          console.log("Still waiting")
        }
      }, RETRY_DELAY);
    })
  }

  /*
    Returns all the CSV files in the current folder as the kernel.
  */
  async getDataFiles(): Promise<string[]> {
    const id = getRandomId();

    this.send({
      'event': 'api_call',
      'type': 'datafiles',
      'id': id
    })

    const dataFiles = await this.getResponseData(id) as string[] | undefined;
    
    if (dataFiles == undefined) {
      return []
    }
    return dataFiles;
  }

  /*
    Import summaries are a mapping from step_id -> import information for each of the 
    import steps in the analysis with the given analysisName.
  */
  async getImportSummary(analysisName: string): Promise<ImportSummaries> {
    const id = getRandomId();

    this.send({
      'event': 'api_call',
      'type': 'import_summary',
      'id': id,
      'analysis_name': analysisName
    })

    const importSumary = await this.getResponseData(id) as ImportSummaries | undefined;
    
    if (importSumary == undefined) {
      return {}
    }
    return importSumary;
  }
}