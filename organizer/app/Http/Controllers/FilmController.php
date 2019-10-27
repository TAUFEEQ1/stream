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
}