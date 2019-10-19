<?php
namespace App;
use Illuminate\Database\Eloquent\Model;
class Actors extends Model{
    protected $table = 'actors';
    public function movies(){
        return $this->hasMany('App\MovieActors');
    }
}