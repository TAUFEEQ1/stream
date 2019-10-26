<template>
    <div>
        <section id="topview">
            <Stream :options="videoOptions"/>
        </section>
        <section id="plot">
        </section>
        <section id="genre">
        </section>
        <section id="cast">    
        </section>
    </div>
</template>
<style scoped>

</style>
<script>
import config from '../config.json';
import Stream from '../components/Stream';
export default {
    components:{
        Stream
    },
    data(){
        return{
            plot:'',
            cast:{},
            movie_id:0,
            src:''
        }
    },
    computed:{
			videoOptions() {
                return {
                    autoplay: true,
                    controls: true,
                    sources: [
                        {
                            src:this.src,
                        }
                    ]
                }

            },
            
    },
    mounted(){
        this.movie_id = this.$route.params.movie_id;
        this.getCast();
        this.getPlot();
    },
    methods:{
        getCast(){
            let movie_id = this.movie_id;
            this.axios({
                url: config.organizer + 'get_cast',
                params:{movie_id:movie_id}
            }).then((response)=>{
                this.cast = response.data;
            });
        },
        getPlot(){
            let movie_id = this.movie_id;
            this.axios({
                url:config.organizer + 'get_synopsis',
                params:{movie_id:movie_id}
            }).then((response)=>{
                this.plot = response.data;
            });
        }
    }
}
</script>