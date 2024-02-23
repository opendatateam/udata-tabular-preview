import { tabular_api_url, tabular_page_size } from "./config";


/**
 * Fetch url
 * @param {string} url url to fetch
 * @returns {object} api result
 */
export function fetchData(url) {
  return fetch(url)
    .then(res => {
      if (!res.ok) {
        throw new Error('Erreur réseau');
      }
      return res.json()
    })
    .then(data => {
      return { data };
    });
}

/**
 * Call Tabular-api to get table content
 * @param {string} id resource id
 * @param {string} page page
 * @param {object} sortConfig sort config 
 * @returns {object} api result
 */
export function getData(id, page, sortConfig) {
  //let url = `${tabular_api_url}/api/resources/${id}/data/?page=${page}&page_size=${tabular_page_size}`; // Construit l'URL avec l'ID
  let url = `${tabular_api_url}/api/resources/3ab0d13c-1ef0-435d-9af4-519c72f46303/data/?page=${page}&page_size=${tabular_page_size}`; // Construit l'URL avec l'ID
  
  if (sortConfig) {
    url = url + `&${sortConfig.column}__sort=${sortConfig.type}`
  }
  return fetchData(url)
}

/**
 * Call Tabular-api to get table profile
 * @param {string} id resource id
 * @returns {object} api result
 */
export function getProfile(id) {
  //let url = `${tabular_api_url}/api/resources/${id}/profile/`; // Construit l'URL avec l'ID
  let url = `${tabular_api_url}/api/resources/91084b11-1316-422e-bccf-b86234cd3fd9/profile/`; // Construit l'URL avec l'ID
  return fetchData(url)
}