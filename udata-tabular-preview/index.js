import 'vite/modulepreload-polyfill';
import { registerComponent, registerTranslation } from "udata-front";
import Explore from "./explore.vue";
import messages from '@intlify/unplugin-vue-i18n/messages';

registerComponent("explore", Explore, "udata-tabular-preview", "explore");
registerTranslation(messages);