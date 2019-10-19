<?php

namespace App\Http\Controllers;

use Laravel\Lumen\Http\Request;

class HomeController extends Controller
{
    public function get_latest(Request $request){
        $count = $request->input('count');
        if($request->has('date1')){
            //Filter by date
        }
        if($request->has('categories')){
            //filter by categories
        }

    }
    
    public function get_popular(Request $request){

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
