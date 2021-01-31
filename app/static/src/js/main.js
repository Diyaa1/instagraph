import Vue from 'vue'
import VueRouter from 'vue-router'
import vuetify from './plugins/vuetify'
import Index from './components/index'
import FollowersSearch from './components/FollowersSearch'
import FollowersBatch from './components/FollowersBatch'
import io from 'socket.io-client';
// Define global packages
window.axios = require('axios');
window.socket = io("https://followerspicker.com/");



Vue.use(VueRouter)

// 2. Define some routes
// Each route should map to a component. The "component" can
// either be an actual component constructor created via
// `Vue.extend()`, or just a component options object.
// We'll talk about nested routes later.
const routes = [
  { path: '/', component: Index, name: "Index" },
  { path: '/followers', component: FollowersSearch, name: "Followers" },
  { path: '/followers-batch/:batchId', component: FollowersBatch, name: "FollowersBatch" },
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = new VueRouter({
  routes // short for `routes: routes`
})

let app = new Vue({
  vuetify,
  router,
  delimiters : ['[[', ']]'],
  data: () => ({
    items: [
      ['mdi-view-dashboard', 'Dashboard', 'Index'],
      ['mdi-account-search-outline', 'Search Followers', "Followers"],
    ],
    drawer: false,
    loggingOut: false
  }),
  methods: {
    logout : function(){
      this.loggingOut = true;
      window.location.href = '/logout';
    } 
  }
}).$mount('#app')
