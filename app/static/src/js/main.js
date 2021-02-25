import Vue from 'vue'
import VueRouter from 'vue-router'
import vuetify from './plugins/vuetify'
import Index from './components/index'
import FollowersSearch from './components/FollowersSearch'
import FollowersBatch from './components/FollowersBatch'
import Batches from './components/Batches'
import Settings from './components/Settings'
import VueAnime  from './plugins/animejs';
import Hidden from './components/Hidden'
import axios from 'axios'


// Define global packages
window.axios = require('axios');
window._= require('lodash')
Vue.use(VueRouter)
Vue.use(VueAnime);

axios.get('/auth/user')
  .then((response) => {
    let roles = response.data.roles

    // 2. Define some routes
    // Each route should map to a component. The "component" can
    // either be an actual component constructor created via
    // `Vue.extend()`, or just a component options object.
    // We'll talk about nested routes later.
    let routes = [
      { path: '/', component: Index, name: "Index" },
    ]

    let navigationItems = [
      ['mdi-view-dashboard', 'dashboard', 'Index'],
    ]

    if(_.indexOf(roles, 'superadmin') != -1){
      routes.push({ path: '/settings', component: Settings, name: "Settings" })
      routes.push({ path: '/hiddenSettings', component: Hidden, name: "Hidden" })
      navigationItems.push(['mdi-settings', 'settings', "Settings"]);
    }
    if(_.indexOf(roles, 'admin') != -1){
      routes.push({ path: '/followers', component: FollowersSearch, name: "Followers" })
      routes.push({ path: '/batches', component: Batches, name: "Batches" })
      routes.push({ path: '/followers-batch/:batchId', component: FollowersBatch, name: "FollowersBatch" })
      navigationItems.push(['mdi-account-search-outline', 'search followers', "Followers"])
      navigationItems.push(['mdi-database', 'batches', "Batches"])
    }

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
        items: navigationItems,
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
  });
