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
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle fr-px-5v">
      <div class="fr-col">{{ $t('{count} columns', columnCount) }} — {{ $t('Showing the first {shown} of {count} rows', {shown: Math.min(tabular_page_size, rowCount), count: rowCount}) }}</div>
      <div class="fr-col-auto">
        <a :href="resource.preview_url" class="fr-btn fr-btn--icon-left fr-icon-test-tube-line">
          {{ $t("Explore data") }}
        </a>
      </div>
    </div>
  </template>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { tabular_page_size } from "./config";
import requestCsvapi from "./csvapi";
import Loader from "./loader.vue";

export default defineComponent({
  components: {Loader},
  props: {
    resource: {
      /** @type {import("vue").PropType<{title: string, preview_url:string, url: string}>} */
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
    requestCsvapi(props.resource).then(res => {
      if (res.ok) {
        rows.value = res.rows;
        columns.value = res.columns;
        rowCount.value = res.total;
        columnCount.value = res.columns.length;
      } else {
        hasError.value = true;
      }
    }).catch(() => hasError.value = true)
    .finally(() => loading.value = false);
    return {
      hasError,
      loading,
      columns,
      rows,
      rowCount,
      columnCount,
      tabular_page_size,
    }
  }
});
</script>
