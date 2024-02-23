import { apify, configure, getData } from "@etalab/explore.data.gouv.fr/lib/csvapi";

/**
 * @typedef {object} CsvapiResponseWithEndpoint
 * @property {string} endpoint - the endpoint for further requests
 * @property {Promise<import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiResponse>} data - data from the first call
 */

/**
 * @type {Map<string, Promise<CsvapiResponseWithEndpoint>>}
 */
const csvapiRequests = new Map();

/**
 * Call Csvapi functions apify and getData with provided configuration.
 * Configuration is called twice : one time before each call to Csvapi.
 *
 * @param {string} url - a url to a resource hosted on udata
 * @param {import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiRequestConfiguration} config - Csvapi configuration
 * @returns {Promise<CsvapiResponseWithEndpoint>}
 */
export default function requestCsvapi(url, config) {
  let existingRequest;
  if(existingRequest = csvapiRequests.get(url)) {
    return existingRequest;
  }
  configure(config);
  const request = apify(url).then(res => {
    if (res.ok) {
      config.dataEndpoint = res.endpoint;
      configure(config);
      return {
        endpoint: res.endpoint,
        data: getData("apify"),
      };
    } else {
      throw new Error("Got 200 but result isn't ok");
    }
  });
  csvapiRequests.set(url, request);
  return request;
}
