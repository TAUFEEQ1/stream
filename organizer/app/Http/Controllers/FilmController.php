<?php

namespace App\Http\Controllers;

use Laravel\Lumen\Http\Request;

class FilmController extends Controller{
    public function get_movie(Request $request){
        $movie_id = $request->input('movie_id');
        $themovie = \App\Movies::find($movie_id);
        $themovie->cast;
        $themovie->plot;
        return \response()->json($themovie);
    }
    public function rate_movie(Request $request){
        $userviews_id = $request->input('userviews_id');
        $ratings = $request->input('ratings');
        //Write to database
        $userviews = \App\UserViews::find($userviews_id);
        $userviews->ratings = $ratings;
        $userviews->save();
        //Set on queue aka message board.
        $user_id = $userviews->id;
        $userRate = 'userRate_'.$user_id;
        $this->app('redis')->rPush($userRate, $userviews_id);
        \App\Jobs\RateJob::dispatch($user_id);
        return \response()->json(["message"=>"operation successful"]);
    } 

}