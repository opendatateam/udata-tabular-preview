import { computed, ref, unref } from "vue";
import { changePage, configure, sort } from "@etalab/explore.data.gouv.fr/lib/csvapi";
import { tabular_csvapi_url, tabular_page_size } from "./config";
import requestCsvapi from "./csvapi";

/**
 *
 * @param {import("./index").Resource} resource
 */
export default function useCsvapi(resource) {
  resource = unref(resource);

  /** @type {import("vue").Ref<Array>} */
  const columns = ref([]);
  const columnsInfos = ref({});
  /** @type {import("vue").Ref<Array>} */
  const rows = ref([]);
  /** @type {import("vue").Ref<number | null>} */
  const columnCount = ref(null);
  const loading = ref(true);
  const hasError = ref(false);
  const currentPage = ref(1);
  const rowCount = ref(0);
  /** @type {import("vue").Ref<string | null>} */
  const dataEndpoint = ref(null);
  const pageSize = Number.parseInt(tabular_page_size ?? "10");
  /** @type {import("vue").Ref<string | null>} */
  const sortBy = ref(null);
  const sortDesc = ref(false);

  /** @type {import("vue").ComputedRef<import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiRequestConfiguration>} */
  const config = computed(() => {
    return {
      csvapiUrl: tabular_csvapi_url,
      dataEndpoint: dataEndpoint.value,
      filters: [],
      page: currentPage.value,
      pageSize: pageSize,
      sortBy: sortBy.value,
      sortDesc: sortDesc.value,
      totalRows: rowCount.value,
    };
  });

  /**
   *
   * @param {import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiResponse} res
   */
  const update = (res) => {
    if (res.ok) {
        rows.value = res.rows;
        columns.value = res.columns;
        columnsInfos.value = res.columns_infos;
        rowCount.value = res.total;
        columnCount.value = res.columns.length;
      } else {
        hasError.value = true;
      }
      return res.ok;
  }

  const onError = () => {
    hasError.value = true;
    return false;
  }

  const changeExplorePage = (page) => {
    configure(config.value);
    const res = changePage(page);
    if(res) {
      res.then(update)
      .catch(() => hasError.value = true)
      .finally(() => loading.value = false);
    }
    currentPage.value = page;
  }

  /**
   *
   * @param {string} col
   */
  const sortbyfield = (col) => {
    if(sortBy.value == col) {
      sortDesc.value = !sortDesc.value;
    } else {
      sortDesc.value = false;
    }
    sortBy.value = col;
    console.log(config.value);
    configure(config.value);
    return sort(sortBy.value, sortDesc.value)
      .then(res => {
        update(res);
        currentPage.value = 1;
      }).catch((e) => {
        console.log(e);
        hasError.value = true;
      })
      .finally(() => loading.value = false);
  };

  /**
   * Check if the preview is sorted by the provided column
   * @param {string} col column name
   * @returns {boolean}
   */
  const isSortedBy = (col) => col === sortBy.value;

  /**
   *  Get data from Csvapi.
   *  It calls apify before and use a local cache.
   *  It handles error and loading state with hasError ref and loading ref.
   * @returns {Promise<boolean>} The boolean tells if the request get data or not
   */
  const apifyAndGetData = () => requestCsvapi(resource.url, config.value)
    .then(({endpoint, data}) => {
      dataEndpoint.value = endpoint;
      return data;
    })
    .then(update)
    .catch(onError)
    .finally(() => loading.value = false);

  return {
    apifyAndGetData,
    changePage: changeExplorePage,
    columns,
    columnCount,
    currentPage,
    hasError,
    isSortedBy,
    loading,
    pageSize,
    rows,
    rowCount,
    sortbyfield,
    sortDesc,
  }
}
