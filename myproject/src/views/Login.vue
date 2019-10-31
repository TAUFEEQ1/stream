<template>
    <v-container>
        <v-row align="center" class="my-5">
            <v-card width="400px" class="mx-auto my-5">
                <h2>Login</h2>
                <v-form ref="form" v-model="valid" class="spacing-playground py-0 px-2">
                    <v-text-field
                        v-model="phoneNo"
                        :counter="10"
                        :rules="phoneNoRules"
                        label="Phone no."
                        required
                    ></v-text-field>
                    <v-btn
                        :disabled="!valid"
                        color="success"
                        class="mr-4 mb-3"
                        @click="login"
                    >
                        LOGIN
                    </v-btn>
                </v-form>
            </v-card>
        </v-row>
    </v-container>
</template>
<script>
import config from '../config.json';
export default {
    name:'Login',
    components:{},
    data(){
        return{
            valid: true,
            phoneNoRules: [
                v => !!v || 'Phone No is required',
                v => (v && v.length == 10) || 'Number must be less than 11 characters',
            ],
            phoneNo:'',
        }
    },
    methods:{
        login(){
            if (this.$refs.form.validate()) {
                let phone_no = this.phoneNo;
                this.axios({
                    url: config.organizer + 'authenticate',
                    data:{phone_no:phone_no},
                    method:"post"
                }).then((response)=>{
                    this.$cookies.set('Api-Token', response.data['auth_key'],'1d','/',window.location.hostname);
                    //route to Home 
                    this.$router.push({ path: '/' });
                });
            }
        }
    }
}
</script>