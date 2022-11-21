<template>
    <div class="fr-table fr-table--no-background fr-p-0 fr-pt-0-5v fr-m-0">
        <table class="fr-mb-3w">
            <caption class="fr-sr-only">{{ $t('Preview of {name}', { name: resource.name }) }}</caption>
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
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col">{{ $t('{count} columns', columnCount) }} — {{ $t('{count} rows', rowCount) }}</div>
        <div class="fr-col-auto">
            <a :href="resource.preview_url" class="fr-btn fr-btn--icon-left fr-icon-test-tube-line">
                {{ $t("Explore data") }}
            </a>
        </div>
    </div>
</template>

<script>
import  { apify, configure, getData } from "@etalab/csvapi-front/src/csvapi";
import { defineComponent, ref } from 'vue';
import { tabular_csvapi_url, tabular_page_size } from "./config";

export default defineComponent({
    props: {
        resource: {
            type: Object,
            required: true
        }
    },
    setup(props) {
        /** @type {import("vue").Ref<Array>} */
        const columns = ref([]);
        /** @type {import("vue").Ref<object | null>} */
        const generalInformations = ref(null);
        /** @type {import("vue").Ref<Array>} */
        const rows = ref([]);
        /** @type {import("vue").Ref<number | null>} */
        const rowCount = ref(null);
        /** @type {import("vue").Ref<number | null>} */
        const columnCount = ref(null);
        const loading = ref(true);
        configure({csvapiUrl: tabular_csvapi_url, pageSize: tabular_page_size});
        // TODO : remove when we're done or find a way to 
        const url = props.resource.latest.replace("http://dev.local:7000", "https://www.data.gouv.fr");
        apify(url).then(res => {
            if (res.ok) {
                configure({dataEndpoint: res.endpoint});
                return getData("apify").then(res => {
                    if (res.ok) {
                        rows.value = res.rows;
                        columns.value = res.columns;
                        generalInformations.value = res.general_infos;
                        rowCount.value = res.total;
                        columnCount.value = res.columns.length;
                    } else {
                        console.log(res);
                    }
                    loading.value = false;
                }).catch(res => console.log(res));
            } else {
                console.log(res);
                loading.value = false;
            }
        }).catch(res => console.log(res));
        return {
            generalInformations,
            columns,
            rows,
            rowCount,
            columnCount,
            loading,
        }
    }
});
</script> 