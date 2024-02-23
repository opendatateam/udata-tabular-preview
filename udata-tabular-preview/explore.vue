<template>
    <div>
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
                  <div class="fr-grid-row fr-grid-row--middle col-width">
                    <button
                      class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline fr-my-n1w"
                      :class="{
                        'fr-btn--secondary-grey-500': !isSortedBy(col),
                        'fr-btn--icon-right': isSortedBy(col),
                        'fr-icon-arrow-down-line': isSortedBy(col) && sortConfig && sortConfig.type == 'desc',
                        'fr-icon-arrow-up-line': isSortedBy(col) && sortConfig && sortConfig.type == 'asc'
                        }"
                      @click="sortByField(col)"
                    >
                      {{ col }}
                      <span class="fr-sr-only">{{ sortConfig && sortConfig.type == 'desc' ? $t("Sort ascending") : $t("Sort descending") }}</span>
                    </button>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in rows" >
                <td v-for="col in columns" class="cell-padding"><div class="style-cell"><div class="content-cell">{{ row[col] }}</div></div></td>
              </tr>
            </tbody>
          </table>
        </div>
        <Pagination
          class="fr-mt-3w"
          :page="currentPage"
          :pageSize="pageSize"
          :totalResults="rowCount"
          :changePage="changePage"
        />
        <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle fr-px-5v">
          <div class="fr-col">{{ $t('{count} columns', columns.length) }} — {{ $t('{count} rows', rowCount) }}</div>
          <div class="fr-col-auto">
            <a :href="resource.preview_url" class="fr-btn fr-btn--icon-left fr-icon-test-tube-line">
              {{ $t("Explore data") }}
            </a>
          </div>
        </div>
      </template>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import getDataTabularApi from "./useTabularapiData.js";
import Loader from "./loader.vue";
import { Pagination } from "@etalab/udata-front-plugins-helper";

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
      changePage,
      getTableInfos,
    } = getDataTabularApi(props.resource)

    getTableInfos(currentPage.value);

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
      changePage,
    };
  }
});
</script>

<style scoped>
.style-cell{
  height: 3rem;
  overflow-y: auto;
  display: block;
  width: 100%;
  font-size: 12px;
  line-height: 20px;
  display: flex;
  align-items: center;
}
.content-cell{
  margin-top: auto;
  margin-bottom: auto;
}
.col-width{
  width: 20rem;
}
.cell-padding{
  padding: 0.5rem 0rem 0.5rem 1.2rem!important
}
td{
  border-right: 1px solid #CECECE;
  border-bottom: 1px solid #CECECE;
}
th{
  border-top: 1px solid black;
  border-right: 1px solid #CECECE;
}
</style>
