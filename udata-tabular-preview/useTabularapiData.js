import { ref, unref } from "vue";
import { tabular_page_size } from "./config";
import { getData } from "./tabularapi";


/**
 *
 * @param {import("./index").Resource} resource
 */
export default function getDataTabularApi(resource) {
  resource = unref(resource);
  /** @type {import("vue").Ref<Array>} */
  const rows = ref([]);
  /** @type {import("vue").Ref<Array>} */
  const columns = ref([]);
  const loading = ref(true);
  const hasError = ref(false);
  const sortConfig = ref({});
  const rowCount = ref(0);
  const pageSize = Number.parseInt(tabular_page_size);
  const currentPage = ref(1);


  /**
   * Check if the preview is sorted by the provided column
   * @param {string} col column name
   * @returns {boolean}
   */
  const isSortedBy = (col) => col === sortConfig.value.column;


  /**
   * Retrieve preview necessary infos
   * @param {number} page current page
   * @param {object} sortConfig sort params 
   */
  const getTableInfos = async (page, sortConfig) => {
    try {
      const { data } = await getData(resource.id, page, sortConfig); // Assurez-vous que cette fonction retourne bien les données attendues
      if ('data' in data && data.data && data.data.length > 0) {
        rows.value = data.data; // Met à jour rows avec les données reçues
        columns.value = Object.keys(data.data[0]).filter(item => item !== "__id");
        rowCount.value = data.meta.total;
        currentPage.value = page;
        loading.value = false
      } else {
        hasError.value = true;
        loading.value = false;
      }
    } catch (error) {
      //console.error("Erreur lors de la récupération des rows:", error);
      hasError.value = true;
      loading.value = false;
    }
  };


  /**
   * Change page
   * @param {number} page requested page
   */
  const changePage = (page) => {
    getTableInfos(page, sortConfig.value)
  }


  /**
   * Sort by a specific column
   * @param {string} col current page
   */
  const sortByField = (col) => {
    if (sortConfig.value && sortConfig.value.column == col){
      if (sortConfig.value.type == "asc") { sortConfig.value.type = "desc" } 
      else { sortConfig.value.type = "asc" }
    } else {
      sortConfig.value.column = col
      sortConfig.value.type = "asc"
    }
    currentPage.value = 1
    getTableInfos(currentPage.value, sortConfig.value)
  };

  return {
    loading,
    hasError,
    rows,
    columns,
    rowCount,
    pageSize,
    currentPage,
    sortConfig,
    isSortedBy,
    sortByField,
    changePage: changePage,
    getTableInfos,
  }
} 