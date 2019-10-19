<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class Userviews extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //
        Schema::create('userviews',function(Blueprint $table){
            $table->bigIncrements('id');
            $table->primary('id');
            $table->foreign('movies_id')
            ->references('id')->on('movies')
            ->onDelete('cascade');
            $table->foreign('user_id')
            ->references('id')->on('user')
            ->onDelete('cascade');
            $table->dateTime('start');
            $table->dateTime('end');
            $table->integer('duration');
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
    }
}
