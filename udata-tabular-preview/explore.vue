<template>
  <div class="bg-alt-green-tilleul-verveine fr-p-3v fr-mt-4w fr-mx-4w fr-mb-3v" v-if="hasError">
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
      v-if="rowCount > pageSize"
      :page="currentPage"
      :pageSize="pageSize"
      :totalResults="rowCount"
      @change="changePage"
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
import { Pagination } from "@etalab/data.gouv.fr-components";
import { defineComponent } from 'vue';
import Loader from "./loader.vue";
import useCsvapi from "./useCsvapi";

export default defineComponent({
  components: {Loader, Pagination},
  props: {
    resource: {
      /** @type {import("vue").PropType<import("./index").Resource>} */
      type: Object,
      required: true
    }
  },
  setup(props) {
    const {
      apifyAndGetData,
      changePage,
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
   } = useCsvapi(props.resource);

    apifyAndGetData();

    return {
      changePage,
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
    };
  }
});
</script>
