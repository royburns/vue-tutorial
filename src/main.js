import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store'

import App from './App'
import 'bootstrap/dist/css/bootstrap.css'
import 'font-awesome/css/font-awesome.css'
import Home from './components/Home'
import Search from './components/Search'
import TimeEntries from './components/TimeEntries'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    component: Home,
    // beforeEnter: (to, from, next) => {
    //     // ...
    // }
},{
    path: '/home',
    // redirect: '/',
    component: Home
},{
    path: '/search',
    // redirect: '/',
    component: Search
},{
    path: '/time-entries',
    component: TimeEntries,
    children: [{
        path: 'log-time',
        component: resolve => require(['./components/LogTime.vue'], resolve)
    }]
}]
const router = new VueRouter( {
    routes
})

/* eslint-disable no-new */
new Vue({
    // el: '#app',
    router,
    store,
    ...App
}).$mount('#app')
