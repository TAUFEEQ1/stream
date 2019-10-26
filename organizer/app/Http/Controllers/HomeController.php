<?php

namespace App\Http\Controllers;

use Laravel\Lumen\Http\Request;

class HomeController extends Controller
{
    public function get_latest(Request $request){
        $filter = $request->all();
        // $thequery = \App\MovieGenre::where('id', $productId)
        // ->leftJoin('movies', 'moviegenre.movies_id', '=', 'moviegenre.id');
        if($filter['daterange']){
            //Filter by date

        }
        if($filter('categories')){
            //filter by categories
        }

    }
    
    public function get_popular(Request $request){
        $collection = \App\UserViews::groupBy('movies_id')
        ->selectRaw('count(*) as total, movies_id')
        ->orderBy('total','desc')
        ->take(12)
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
