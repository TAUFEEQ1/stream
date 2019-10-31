import VueRouter from 'vue-router';
import Home from '../views/Home';
import Login from '../views/Login';
const routes = [
    {
        path:'/',
        component:Home
    },
    {
        path:'/login',
        component:Login
    }
];
const router = new VueRouter({
    routes // short for `routes: routes`
});

export default router