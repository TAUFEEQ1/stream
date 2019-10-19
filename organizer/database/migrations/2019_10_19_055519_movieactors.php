<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class Movieactors extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //
        Schema::create('movieactors',function(Blueprint $table){
            $table->bigIncrements('id');
            $table->integer('movies_id');

            $table->foreign('movies_id')
            ->references('id')->on('movies')
            ->onDelete('cascade');
            
            $table->integer('actors_id');
            
            $table->foreign('actors_id')
            ->references('id')->on('actors')
            ->onDelete('cascade');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //
        Schema::drop('movieactors');
    }
}
