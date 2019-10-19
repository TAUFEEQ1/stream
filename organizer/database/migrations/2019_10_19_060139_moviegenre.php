<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class Moviegenre extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //
        Schema::create('moviegenre',function(Blueprint $table){
            $table->bigIncrements('id');
            $table->primary('id');
            $table->foreign('movies_id')
            ->references('id')->on('movies')
            ->onDelete('cascade');
            $table->foreign('genre_id')
            ->references('id')->on('genre')
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
        Schema::drop('moviegenre');
    }
}
