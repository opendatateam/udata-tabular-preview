import { ref, unref } from "vue";
import { getProfile } from "./tabularapi";


/**
 *
 * @param {import("./index").Resource} resource
 */
export default function getProfileTabularApi(resource) {
  resource = unref(resource);
  /** @type {import("vue").Ref<Array>} */
  const columns = ref([]);
  const columnsInfos = ref({})
  const loading = ref(true);
  const hasError = ref(false);
  const hasColumnInfos = ref(false);

  /**
   * Retrieve profile from a resource
   */
  const getProfileInfos = async () => {
    try {
      const { data } = await getProfile(resource.id); // Assurez-vous que cette fonction retourne bien les données attendues
      if ('profile' in data && data.profile) {
        columns.value = Object.keys(data.profile.columns)
        columnsInfos.value = data.profile.columns
        hasColumnInfos.value = true
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

  return {
    loading,
    hasError,
    hasColumnInfos,
    columns,
    columnsInfos,
    getProfileInfos,
  };
}