<?php
namespace App;
use Illuminate\Database\Eloquent\Model;
class Genre extends Model{
    protected $table = 'genre';
    public function movies(){
        return $this->hasMany('App\MovieGenre');
    }
}