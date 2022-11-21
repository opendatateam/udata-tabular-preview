/**
 * Simple helper to fetch attribute on given css selector
 * @param {string} selector
 * @param {string} name
 */
function _attr(selector, name) {
    const el = document.querySelector(selector);
    return el ? el.getAttribute(name) : null;
}

/**
 * Simple helper to <meta/> tag content given its name
 * @param {string} name
 */
function _meta(name) {
    return _attr(`meta[name=${name}]`, "content");
}

export const tabular_csvapi_url = _meta("tabular-csvapi-url");
export const tabular_page_size = _meta("tabular-page-size");