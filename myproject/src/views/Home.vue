<template>
<v-sheet height="600" class="overflow-hidden" style="position: relative;" width="350">
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
            <v-list-group value="true">
                <template v-slot:activator>
                <v-list-item-title>Genre</v-list-item-title>
                </template>
                <v-list-item v-for ="(k,index) in genres" :key="'gen'+index">
                    <v-checkbox 
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
                        ></v-radio>
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
            <h3 class="ml-3">Latest Movies</h3>
            <head-view :latest="latest"></head-view>
        </v-row>
        <v-row>
            <v-btn @click="searching">
                Search
            </v-btn>
            <v-btn @click="drawer=!drawer" color="info">
                Menu
            </v-btn>
            <recommended  :recom="recom" dark></recommended>
        </v-row>
    </v-container>
</v-sheet>
</template>
<style scoped>

</style>
<script>
import config from '../config.json'
import HeaderView from '../components/HeaderView'
import Recommended from '../components/Recommended'
import moment from 'moment'
export default {
    data(){
        return{
            latest:[],
            drawer: null,
            recom:[],
            selcats:[],
            switch1:false,
            filtering:false,
            popular:[],
            radios:'',
            thedata:{},
            genres:[]
        }
    },
    watch:{
        selcats: function(){
            if(this.selcats.length > 0){
                this.thedata['catgeories'] = this.selcats;
                console.log(this.selcats)
            }
        },
        radios:function(theval){
            let yesterday,date2,lastmonth,threemonth,lastweek = Date();
            let interest = []
            if(theval){
                switch(theval){
                    case "yesterday":
                        yesterday = moment().subtract(1, 'day').toDate();
                        date2 = moment();
                        interest = [yesterday,date2];
                        this.thedata['daterange'] = interest;
                        break;
                    case "lastweek":
                        lastweek = moment().subtract(7,'day').toDate();
                        date2 = moment();
                        this.thedata['daterange'] = [lastweek,date2];
                        break;
                    case "lastmonth":
                        lastmonth = moment().subtract(30,'day').toDate();
                        date2 = moment();
                        this.thedata['daterange'] = [lastmonth,date2];
                        break;
                    case "threemonths":
                        threemonth = moment().subtract(90,'day').toDate();
                        date2 = moment();
                        this.thedata['daterange'] = [threemonth,date2];
                        break;
                }

            }
        }

    },
    components:{
        'head-view':HeaderView,
        'recommended':Recommended
    },
    created(){
        if(!this.$cookies.get('Api-Token')){
            this.$router.push({path:'/login'});
        }
    },
    mounted(){
        this.getlatest();
        this.get_genres();
    },
    methods:{
        getlatest(){
            this.axios({
                url:config.organizer + 'get_latest',
                data:this.thedata,
                headers:{'Api-Token':this.$cookies.get('Api-Token')}
            }).then((response)=>{
                this.latest = response.data;
            });
        },
        getpopular(){
            this.axios({
                url:config.organizer + 'get_popular',
                data:this.thedata
            }).then((response)=>{
                this.popular = response.data;
            });
        },
        getrecommended(){
            this.axios({
                url:config.analyzer +'get_recommended',
                data:this.thedata
            }).then((response)=>{
                //Recommended
                this.recom = response.data;
            });
        },
        get_genres(){
            this.axios({
                url:config.organizer + 'get_genres',
            }).then((response)=>{
                this.genres=response.data;
            });
        },
        searching(){
            //this.getrecommended();
            this.getlatest();
            //this.getpopular();
        }
    }
}
</script>