<template>
    <div>
        <carousel style="width:80vh;" :width="280" :height="360">
            <slide
                v-for="(j,index) in latest"
                :key="'latest'+index"
            >
                <figure>
                    <v-img 
                        :src="'/images/'+j.mposter+'/1.jpg'"
                        max-width="200"
                        max-height="200"
                        class="grey lighten-2"
                    ></v-img>
                    <figcaption>
                        <h4>{{j.title}}</h4>
                    </figcaption>
                </figure>
            </slide>
        </carousel>
    </div>
</template>
<style scoped>

</style>
<script>
export default {
    props:['latest'],
    components:{
    },
    
}
</script>