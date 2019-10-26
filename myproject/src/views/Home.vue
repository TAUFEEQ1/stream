<template>
<v-sheet height="400" class="overflow-hidden" style="position: relative;">
    <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
    >
        <v-list-item>
        <v-list-item-avatar>
            <v-img src="https://randomuser.me/api/portraits/men/78.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
            <v-list-item-title>John Leider</v-list-item-title>
        </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list dense>
            <v-list-group prepend-icon="account_circle" value="true">
                <template v-slot:activator>
                <v-list-item-title>Genre</v-list-item-title>
                </template>
                <v-list-item>
                    <v-checkbox
                    v-for ="(k,index) in genres"
                    :key="'gen'+index" 
                    v-model="selcats" 
                    :label="k.genre"
                    :value="k.id"
                    ></v-checkbox>
                </v-list-item>
            </v-list-group>
            <v-list-group>
                <template v-slot:activator>
                    <v-list-item-title>
                        Time frames.
                    </v-list-item-title>
                </template>
                <v-list-item>
                    <v-radio-group v-model="radios" :mandatory="false">
                        <v-radio
                            label="Yesterday"
                            value="yesterday"
                        >
                        </v-radio>
                        <v-radio 
                            label="Last Week" 
                            value="lastweek">
                        </v-radio>
                        <v-radio
                            label="Last Month"
                            value="lastmonth"
                        >
                        <v-radio
                            label="Last 3 Months"
                            value="threemonths"
                        >
                        </v-radio>
                    </v-radio-group>
                </v-list-item>
            </v-list-group> 
        </v-list>
    </v-navigation-drawer>
    <v-container class="fill-height">
        <v-row
        >
            <header-view :latest="latest"></header-view>
            <v-btn @click="searching">
                Search
            </v-btn>
            <recommended  :recom="recom"></recommended>
            <most-popular :popular="popular"></most-popular>
        </v-row>
    </v-container>
</v-sheet>
</template>
<script>
import config from '../config.json'
import HeaderView from '../components/HeaderView'
import Recommended from '../components/Recommended'
import MostPopular from '../components/MostPopular'
import moment from 'moment'
export default {
    data(){
        return{
            latest:[],
            drawer: null,
            recom:[],
            selcats:[],
            daterange:[],
            switch1:false,
            filtering:false,
            popular:[],
            radios:'',
            thedata:{}
        }
    },
    watch:{
        selcats: function(){
            if(this.selcats.length > 0){
                this.thedata['catgeories'] = this.selcats
            }
        },
        radios:function(theval){
            if(theval){
                switch(theval){
                    case "yesterday":
                        let yesterday = moment().subtract(1, 'day').toDate();
                        let date2 = moment();
                        interest = [yesterday,date2];
                        break;
                    case "lastweek":
                        break;
                    case "lastmonth":
                        break;
                    case "threemonths":
                        break;
                }

            }
        }

    },
    components:{
        'head-view':HeaderView,
        'recommended':Recommended,
        'most-popular':MostPopular
    },
    created(){
        if(!this.$cookies.get('Api-Token')){
            this.$router.push({path:'/login'});
        }
    },
    methods:{
        getlatest(){
            let theval = this.radios;
            let interest = [];

            this.axios({
                url:config.organizer + 'get_latest',
                data: {

                }
            }).then((response)=>{
                this.latest = response.data;
            });
        },
        getpopular(){
            this.axios({
                url:config.organizer + 'get_popular',
                data:thefilter
            }).then((response)=>{
                this.popular = response.data;
            });
        },
        getrecommended(){
            let thefilter = this.filters;
            this.axios({
                url:config.analyzer +'get_recommended',
                data:thefilter
            }).then((response)=>{
                //Recommended
                this.recom = response.data;
            });
        },
        searching(){
            this.getrecommended();
            this.getlatest();
            this.getpopular();
        }
    }
}
</script>