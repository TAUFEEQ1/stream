<template>
    <div>
        <carousel :paginationEnabled="false" :perPage="1" :navigationEnabled="true">
            <slide
                v-for="(j,index) in latest"
                :key="'latest'+index"
                class="pl-2"
            >   
                <v-card height="340" width="340" >
                    <v-img 
                        :src="'/images/'+j.mposter+'/1.jpg'"
                        max-width="340"
                        max-height="280"
                        class="grey lighten-2"
                    ></v-img>
                    <v-card-text>
                        <h4>{{j.title}}</h4>
                        {{j.created_at}}
                    </v-card-text>
                </v-card>
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