import 'vite/modulepreload-polyfill';
import { registerComponent } from "udata-front";
import Explore from "./explore.vue";

registerComponent("explore", Explore, "udata-tabular-preview", "explore");