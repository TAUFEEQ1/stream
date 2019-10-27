<?php

namespace App\Jobs;
use GuzzleHttp\Client;
class RateJob extends Job
{
    /**
     * Create a new job instance.
     *
     * @return void
     */
    private $user_id;
    public function __construct($user_id)
    {
        //
        $this->user_id = $user_id;
    }

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        //
        $client = new Client([
            // Base URI is used with relative requests
            'base_uri' => env('analyzer'),
            // You can set any number of default request options.
            'timeout'  => 2.0,
        ]);
        $params = [
            'query' => [
               'user_id' => $this->user_id
            ]
         ];
        $client->request('GET', '/onrate',$params);
    }
}
