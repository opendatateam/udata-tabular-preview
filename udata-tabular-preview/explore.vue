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
            <th scope="col" v-for="col in columns">{{ col }}</th>
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
import { apify, changePage, configure, getData } from "@etalab/explore.data.gouv.fr/lib/csvapi";
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

    const changeExplorePage = (page) => {
      const res = changePage(page);
      if(res) {
        res.then(updateData)
        .catch(() => hasError.value = true)
        .finally(() => loading.value = false);
      }
      currentPage.value = page;
    }

    /**
     *
     * @param {import("@etalab/explore.data.gouv.fr/lib/csvapi").CsvapiResponse} response
     */
    const updateData = (response) => {
      if (response.ok) {
        rows.value = response.rows;
        columns.value = response.columns;
        rowCount.value = response.total;
        columnCount.value = response.columns.length;
        totalRows.value = response.total;
        configure({totalRows: totalRows.value});
      } else {
        hasError.value = true;
      }
    }

    configure({ csvapiUrl: tabular_csvapi_url, pageSize, currentPage: currentPage.value });
    apify(props.resource.url).then(res => {
      if (res.ok) {
        configure({ dataEndpoint: res.endpoint });
        return getData("apify")
        .then(updateData)
        .catch(() => hasError.value = true)
        .finally(() => loading.value = false);
      } else {
        hasError.value = true;
        loading.value = false;
      }
    }).catch(() => {
      hasError.value = true;
      loading.value = false;
    });

    return {
      hasError,
      loading,
      columns,
      rows,
      rowCount,
      columnCount,
      currentPage,
      pageSize,
      totalRows,
      changeExplorePage,
    }
  }
});
</script>
