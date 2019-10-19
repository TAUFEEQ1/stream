<template>
    <div>
        <carousel-3d style="width:150vh;" :width="280" :height="360" :space="10">
            <slide
                v-for="(j,index) in latest"
                :key="'latest'+index"
            >
                <figure>
                    <v-img 
                        :src="'/images/'+j.mposter"
                        max-width="200"
                        max-height="200"
                        class="grey lighten-2"
                    ></v-img>
                    <figcaption>
                        <h4>{{j.title}}</h4>
                    </figcaption>
                </figure>
            </slide>
        </carousel-3d>
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