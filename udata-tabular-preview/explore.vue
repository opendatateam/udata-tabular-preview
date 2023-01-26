<template>
  <div class="bg-alt-green-tilleul-verveine fr-p-3v fr-my-2w" v-if="hasError">
    <p class="fr-grid-row fr-m-0">
      <span class="fr-icon-warning-line" aria-hidden="true"></span>
      {{ $t("The preview of this file failed to load.") }}
    </p>
  </div>
  <Loader v-if="loading" />
  <template v-if="!hasError && !loading">
    <div class="fr-table fr-table--no-background fr-p-0 fr-pt-0-5v fr-m-0">
      <table class="fr-mb-3w">
        <caption class="fr-sr-only">{{ $t('Preview of {name}', { name: resource.title }) }}</caption>
        <thead>
          <tr>
            <th scope="col" v-for="col in columns">
              <div class="fr-grid-row fr-grid-row--middle no-wrap">
                <button
                  class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline fr-my-n1w"
                  :class="{
                    'fr-btn--secondary-grey-500': !isSortedBy(col),
                    'fr-btn--icon-right': isSortedBy(col),
                    'fr-icon-arrow-down-line': isSortedBy(col) && sortDesc,
                    'fr-icon-arrow-up-line': isSortedBy(col) && !sortDesc
                    }"
                  @click="sortbyfield(col)"
                >
                  {{ col }}
                  <span class="fr-sr-only">{{ sortDesc ? $t("Sort ascending") : $t("Sort descending") }}</span>
                </button>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows">
            <td v-for="col in columns">{{ row[col] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <Pagination
      class="fr-mt-3w"
      v-if="totalRows > pageSize"
      :page="currentPage"
      :pageSize="pageSize"
      :totalResults="totalRows"
      :changePage="changeExplorePage"
    />
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle fr-px-5v">
      <div class="fr-col">{{ $t('{count} columns', columnCount) }} — {{ $t('{count} rows', rowCount) }}</div>
      <div class="fr-col-auto">
        <a :href="resource.preview_url" class="fr-btn fr-btn--icon-left fr-icon-test-tube-line">
          {{ $t("Explore data") }}
        </a>
      </div>
    </div>
  </template>
</template>

<script>
import { apify, changePage, configure, getData, sort } from "@etalab/explore.data.gouv.fr/lib/csvapi";
import { Pagination } from "@etalab/udata-front-plugins-helper";
import { defineComponent, ref } from 'vue';
import { tabular_csvapi_url, tabular_page_size } from "./config";
import Loader from "./loader.vue";

export default defineComponent({
  components: {Loader, Pagination},
  props: {
    resource: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    /** @type {import("vue").Ref<Array>} */
    const columns = ref([]);
    /** @type {import("vue").Ref<Array>} */
    const rows = ref([]);
    /** @type {import("vue").Ref<number | null>} */
    const rowCount = ref(null);
    /** @type {import("vue").Ref<number | null>} */
    const columnCount = ref(null);
    const loading = ref(true);
    const hasError = ref(false);
    const currentPage = ref(1);
    const pageSize = tabular_page_size;
    const totalRows = ref(0);
    /** @type {import("vue").Ref<string | null>} */
    const sortBy = ref(null);
    const sortDesc = ref(false);

    /**
     *
     * @param {import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiResponse} res
     */
    const update = (res) => {
      if (res.ok) {
          rows.value = res.rows;
          columns.value = res.columns;
          rowCount.value = res.total;
          columnCount.value = res.columns.length;
          totalRows.value = res.total;
          configure({totalRows: totalRows.value});
        } else {
          hasError.value = true;
        }
    }

    const changeExplorePage = (page) => {
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
        sortDesc.value = !sortDesc.value
      } else {
        sortDesc.value = false
      }
      sortBy.value = col;
      return sort(sortBy.value, sortDesc.value).then(res => {
        update(res);
        currentPage.value = 1;
      }).catch(() => hasError.value = true)
      .finally(() => loading.value = false);
    };

    const requestData = () => {
      loading.value = true;
      return getData("apify").then(res => {
        update(res);
      }).catch(() => hasError.value = true)
      .finally(() => loading.value = false);
    }

    const requestApify = () => {
      return apify(props.resource.url).then(res => {
        if (res.ok) {
          configure({ dataEndpoint: res.endpoint });
          return requestData();
        } else {
          hasError.value = true;
          loading.value = false;
        }
      }).catch(() => {
        hasError.value = true;
        loading.value = false;
      });
    }

    const isSortedBy = (col) => col === sortBy.value;

    configure({ csvapiUrl: tabular_csvapi_url, pageSize, currentPage: currentPage.value });

    requestApify();

    return {
      hasError,
      loading,
      columns,
      rows,
      rowCount,
      columnCount,
      sortbyfield,
      isSortedBy,
      sortDesc,
      currentPage,
      pageSize,
      totalRows,
      changeExplorePage,
    };
  }
});
</script>
