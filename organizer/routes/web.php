<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/authenticate','HomeController@authenticate');
$router->group(['middleware' => 'auth'], function () use ($router) {
    $router->get('/get_latest','HomeController@get_latest');
});
$router->get('/', function () use ($router) {
    return $router->app->version();
});
