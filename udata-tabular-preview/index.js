import 'vite/modulepreload-polyfill';
import { registerComponent, registerTranslation } from "@etalab/udata-front-plugins-helper";
import Explore from "./explore.vue";
import messages from '@intlify/unplugin-vue-i18n/messages';

registerComponent("explore", Explore, "udata-tabular-preview", "explore");
registerTranslation(messages, "udata-tabular-preview");
