import 'vite/modulepreload-polyfill';
import { registerComponent, registerTranslation } from "@etalab/udata-front-plugins-helper";
import DataStructure from "./data-structure.vue";
import Explore from "./explore.vue";
import messages from '@intlify/unplugin-vue-i18n/messages';

/**
 * @typedef {{title: string, preview_url:string, url: string}} Resource
 */

registerComponent("explore", Explore, "udata-tabular-preview", "explore");
registerComponent("data-structure", DataStructure, "udata-tabular-preview", "data-structure");
registerTranslation(messages, "udata-tabular-preview");
