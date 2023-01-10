import { apify, configure, getData } from "@etalab/explore.data.gouv.fr/lib/csvapi";
import { tabular_csvapi_url, tabular_page_size } from "./config";

/**
 * @type {Map<string, Promise<import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiResponse>>}
 */
const csvapiRequests = new Map();

/**
 *
 * @param {{url: string}} resource - a resource hosted on udata
 * @returns {Promise<import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiResponse>}
 */
export default function requestCsvapi({url}) {
  configure({ csvapiUrl: tabular_csvapi_url, pageSize: tabular_page_size });

  let existingRequest;
  if(existingRequest = csvapiRequests.get(url)) {
    return existingRequest;
  }

  const request = apify(url).then(res => {
    if (res.ok) {
      configure({ dataEndpoint: res.endpoint });
      return getData("apify");
    } else {
      throw new Error("Got 200 but result isn't ok");
    }
  });
  csvapiRequests.set(url, request);
  return request;
}
