<template>
  <div class="bg-alt-green-tilleul-verveine fr-p-3v fr-mb-2w" v-if="hasError">
    <p class="fr-grid-row fr-m-0">
      <span class="fr-icon-warning-line" aria-hidden="true"></span>
      {{ $t("The data structure of this file failed to load.") }}
    </p>
  </div>
  <Loader v-if="loading" />
  <div v-if="!hasError && !loading" class="fr-grid-row fr-grid-row--gutters">
    <div class="bg-alt-green-tilleul-verveine fr-p-3v fr-mb-2w" v-if="!hasColumnInfos">
      <p class="fr-grid-row fr-m-0">
        <span class="fr-icon-warning-line" aria-hidden="true"></span>
        {{ $t("No data structure found for this file.") }}
      </p>
    </div>
    <div v-if="hasColumnInfos" class="fr-col-12 fr-col-sm-6 fr-col-md-4 fr-col-lg-3" v-for="column in columns">
      <h5 class="fr-text--sm fr-text--bold fr-mt-0 fr-mb-1v">{{column}}</h5>
      <code class="code">
        {{ columnsInfos[column].format }}
      </code>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent } from 'vue';
import Loader from "./loader.vue";
import getProfileTabularApi from "./useTabularapiProfile.js";


export default defineComponent({
  components: {Loader},
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
      hasColumnInfos,
      columns,
      columnsInfos,
      getProfileInfos,
    } = getProfileTabularApi(props.resource);

    getProfileInfos();

    return {
      loading,
      hasError,
      hasColumnInfos,
      columns,
      columnsInfos,
    };
  }
});
</script>
