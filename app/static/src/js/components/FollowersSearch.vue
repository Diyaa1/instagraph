<template>
    <div>
        <v-container style="height: 400px;" v-if="searching">
            <v-row
                class="fill-height"
                align-content="center"
                justify="center"
            >
                <v-col
                class="subtitle-1 text-center"
                cols="12"
                >
                    {{processMsg}}
                </v-col>
                <v-col cols="6">
                <v-progress-linear
                    color="deep-purple accent-4"
                    indeterminate
                    rounded
                    height="12"
                ></v-progress-linear>
                </v-col>
            </v-row>
        </v-container>
        <v-card v-if="!searching" class="mx-auto my-12" max-width="600" :loading="searching" :disabled="searching" ref="form">
            <template slot="progress">
                <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-img height="250" src="/images/instagram.png"></v-img>

            <v-card-title>Search Form</v-card-title>

            <v-card-text>
                <v-row>
                    <v-col cols="12" md="12">
                        <v-text-field 
                            ref="searchUser"
                            v-model="searchUser"  
                            :rules="[rules.required]"
                            label="Searched User" 
                            required
                        ></v-text-field>
                    </v-col>    
                </v-row>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>

            <v-card-actions>
                <v-btn color="deep-purple lighten-2" text @click="search">
                    Search
                </v-btn>
            </v-card-actions>
        </v-card>
        <v-alert max-width="600" style="margin:0 auto" type="error" :value="errorIsVisible">
            {{ errorMessage }}
        </v-alert>
    </div>
</template>

<script>

    module.exports = {
        data: function () {
            return {
                show1: false,
                show2: true,
                show3: false,
                show4: false,
                password: null,
                loginName: null,
                searchUser: null,
                processMsg: "Batch Request Sent",
                searching:false,
                rules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                    emailMatch: () => (`The email and password you entered don't match`),
                },
                errorMessage: "",
                errorIsVisible: false,
                fetchedFollowers: 0
            }
        },
        computed: {
            form() {
                return {
                    searchUser: this.searchUser,
                }
            },
        },
        methods: {
            search: function () {
                this.formHasErrors = false;
                this.errorIsVisible = false;

                Object.keys(this.form).forEach(f => {
                if (!this.form[f]) 
                    this.formHasErrors = true
                    this.$refs[f].validate(true)
                })

                if(this.formHasErrors){
                    return;
                }

                this.searching = true;

                axios({
                    method: 'post',
                    url: '/followers/',
                    data: {
                        searchUser: this.searchUser
                    }
                }).then((response) => {
                    this.batchId = response.data.batch_id;
                    this.statusCheckLoop();
                }, (error) => {
                    if(error.response.status == 429){
                        let code = 429;
                        this.errorIsVisible = true;
                        this.searching = false;
                        this.errorMessage = "Only one request can be sent in 1 minute (Wait for 1 minute)"
                    }else{
                        let data = error.response.data;
                        let code = data.code;
                        this.errorIsVisible = true;
                        this.errorMessage = data.message;
                        this.searching = false;
                    }
                });

            },
            statusCheckLoop:function(){
                axios({
                    method: 'get',
                    url: '/followers/batches/' + this.batchId + "/status",
                }).then((response) => {
                    if(response.data.status == "WORKING"){
                        this.fetchedFollowers = response.data.fetched_count
                        this.processMsg = "Batch is in process " + this.fetchedFollowers + "Followers fetched" 
                        setTimeout(this.statusCheckLoop, 4000);
                    }else if(response.data.status == "DISPATCHED"){
                        this.processMsg = "Batch is dispatched and waiting for worker";
                        setTimeout(this.statusCheckLoop, 4000);
                    }else{
                        this.$router.push({ name: 'FollowersBatch', params: { batchId : this.batchId } })
                    }
                }, (error) => {
                    console.log(error);
                });

            }
        },
        created: function(){
            let self = this;
        }
    };
</script>