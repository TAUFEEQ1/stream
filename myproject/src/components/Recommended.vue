<template>
    <div>
        <h4>Recommended</h4>
        <carousel  :navigationEnabled=true :autoplay="true" class="mt-2"
        paginationActiveColor="#42b983" paginationColor="#b2ebd1" :perPage="2">
            <slide
                v-for="(p,index) in recom"
                :key="'recom'+index"
            >
                <figure>
                    <v-img 
                        :src="'/images/'+p.mposter"
                        max-width="200"
                        max-height="200"
                        class="grey lighten-2"
                    ></v-img>
                    <figcaption>
                        <h4>{{p.title}}</h4>
                    </figcaption>
                </figure>
            </slide>
        </carousel>
    </div>
</template>
<script>
export default {
    props:['recom']
}
</script>
