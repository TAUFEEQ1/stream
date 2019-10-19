<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class Ordercontent extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //
        Schema::create('ordercontent',function(Blueprint $table){
            $table->bigIncrements('id');
            $table->integer('order_id');
            $table->foreign('order_id')
            ->references('id')->on('order')
            ->onDelete('cascade');
            $table->integer('ordertype_id');
            $table->foreign('ordertype_id')
            ->references('id')->on('ordertype')
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
        Schema::drop('ordercontent');
    }
}
