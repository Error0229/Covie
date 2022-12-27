import {createRouter, createWebHistory} from 'vue-router'
import yahoo from '../src/components/yahoo.vue'
import imdb from '../src/components/imdb.vue'
import rotten_tomatoes from '../src/components/rotten_tomatoes.vue'
const routes = [
    {path: '/yahooresult', name: 'yahooResult',component: yahoo},
    {path: '/imdbresult',name :"imdbResult" ,component: imdb},
    {path: '/rottentomatoesresult',name:'rottenTomatoesResult',component: rotten_tomatoes}
];
const router = createRouter({
    history: createWebHistory(),
    routes
});
export default router;

