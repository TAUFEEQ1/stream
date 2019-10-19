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
            $table->primary('id');
            $table->foreign('movies_id')
            ->references('id')->on('movies')
            ->onDelete('cascade');
            $table->foreign('movies_id')
            ->references('id')->on('movies')
            ->onDelete('cascade');
            $table->foreign('actors_id')
            ->references('id')->on('actors')
            ->onDelete('cascade');
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
