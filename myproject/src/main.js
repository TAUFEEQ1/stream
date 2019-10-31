import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import VueCarousel from 'vue-carousel';
import VueRouter from 'vue-router';
import VueCookies from 'vue-cookies';
import axios from 'axios';
import VueAxios from 'vue-axios';
import store from './store';
// import VueWebsocket from "vue-websocket";
import router from './plugins/router';
// Vue.use(VueWebsocket, "ws://otherserver:8080");
Vue.use(VueCookies);
Vue.use(VueAxios, axios);
Vue.config.productionTip = false;
Vue.use(VueCarousel);
Vue.use(VueRouter);
new Vue({
    vuetify,
    router,
    store,
    render: h => h(App)
}).$mount('#app');