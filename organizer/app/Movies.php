<?php
namespace App;
use Illuminate\Database\Eloquent\Model;
class Movies extends Model{
    protected $table="movies";
    public function cast(){
        return $this->hasMany('App\MovieActors');
    }
    public function plot(){
        return $this->hasMany('App\Synopsis');
    }
}