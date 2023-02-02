<template>
  <div class="bg-alt-green-tilleul-verveine fr-p-3v fr-my-2w" v-if="hasError">
    <p class="fr-grid-row fr-m-0">
      <span class="fr-icon-warning-line" aria-hidden="true"></span>
      {{ $t("The data structure of this file failed to load.") }}
    </p>
  </div>
  <Loader v-if="loading" />
  <div v-if="!hasError && !loading" class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-sm-6 fr-col-md-4 fr-col-lg-3" v-for="column in columns">
      <h5 class="fr-text--sm fr-text--bold fr-mt-0 fr-mb-1v">{{column}}</h5>
      <code class="code">
        {{ columnsInfos[column].format }}
      </code>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import requestCsvapi from './csvapi';
import Loader from "./loader.vue";

export default defineComponent({
  components: {Loader},
  props: {
    resource: {
      /** @type {import("vue").PropType<{url: string}>} */
      type: Object,
      required: true
    }
  },
  setup(props) {
    /** @type {import("vue").Ref<Array>} */
    const columns = ref([]);
    const columnsInfos = ref({});
    const loading = ref(true);
    const hasError = ref(false);

    requestCsvapi(props.resource).then(res => {
          if (res.ok) {
            columns.value = res.columns;
            columnsInfos.value = res.columns_infos;
          } else {
            hasError.value = true;
          }
        }).catch(() => hasError.value = true)
        .finally(() => loading.value = false);
    return {
      hasError,
      loading,
      columns,
      columnsInfos,
    }
  }
});
</script>
