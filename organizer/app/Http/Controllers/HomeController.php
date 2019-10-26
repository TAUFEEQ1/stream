<?php

namespace App\Http\Controllers;

use Laravel\Lumen\Http\Request;

class HomeController extends Controller
{
    public function get_latest(Request $request){
        $filter = $request->all();
        // $thequery = \App\MovieGenre::where('id', $productId)
        // ->leftJoin('movies', 'moviegenre.movies_id', '=', 'moviegenre.id');
        $thequery = DB::table('moviegenre')
        ->join('movies', 'moviegenre.movies_id', '=', 'movies.id');
        if($filter['daterange']){
            $dates = $filter['daterange'];
            //Filter by date
            $thequery->whereBetween(
                'movies.created_at',
                [$dates[0],$dates[1]]);
        }
        if($filter['categories']){
            $categories = $filter['categories'];
            //filter by categories
            $thequery->whereIn('genres_id',$categories);
        }
        $movies = $thequery->take(10)->get();
        return response()->json($movies);
    }
    
    public function get_popular(Request $request){
        $collection = \App\UserViews::groupBy('movies_id')
        ->selectRaw('count(*) as total, movies_id')
        ->orderBy('total','desc')
        ->take(10)
        ->get();
        $themovies = array();
        foreach($collection as $movie){
            $themovie = \App\Movies::find($movie->movies_id);
            array_push($themovies, $themovie);
        }
        return response()->json($collection);
    }
    public function authenticate(Request $request){
        $phone_no = $request->input('phone_no');
        $user = App\User::where('phone_no',$phone_no)->first();
        if($user){
            return response()->json([
                'user_id'=>$user->id,
                'auth_key'=>$user->api_token
                ]);
        }else{
            return response()->status(401)->json(['message'=>'User doesnt exist']);
        }
    }
    public function getUserId(Request $request){
        $api_token = $request->header('Api-Token');
        $user = App\User::find($api_token);
        if($user){
            return \response()->json(['user_id'=>$user->id]);
        }else{
            return \response()->status(401)->json(['message'=>'Unauthorized']);
        }
    }
}
