import Vue from 'vue'
import vuetify from './plugins/vuetify' // path to vuetify export

Vue.config.delimiters = ['[[', ']]']

let app = new Vue({
  vuetify
}).$mount('#app')