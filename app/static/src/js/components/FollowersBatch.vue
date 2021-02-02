<style>

.gradient-text {
  /* Fallback: Set a background color. */
  background-color: #CA4246;
  
  /* Create the gradient. */
  background-image: linear-gradient(
        45deg,
        #CA4246 16.666%, 
        #E16541 16.666%, 
        #E16541 33.333%, 
        #F18F43 33.333%, 
        #F18F43 50%, 
        #8B9862 50%, 
        #8B9862 66.666%, 
        #476098 66.666%, 
        #476098 83.333%, 
        #A7489B 83.333%);
  
  /* Set the background size and repeat properties. */
  background-size: 100%;
  background-repeat: repeat;

  /* Use the text as a mask for the background. */
  /* This will show the gradient as a text color rather than element bg. */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; 
  
  /* Animate the text when loading the element. */
    /* This animates it on page load and when hovering out. */
    animation: rainbow-text-simple-animation-rev 0.75s ease forwards;

}

.gradient-text:hover{
    animation: rainbow-text-simple-animation 0.5s ease-in forwards;
}


/* Move the background and make it smaller. */
/* Animation shown when entering the page and after the hover animation. */
@keyframes rainbow-text-simple-animation-rev {
    0% {
        background-size: 650%;
    }
    40% {
        background-size: 650%;
    }
    100% {
        background-size: 100%;
    }
}

/* Move the background and make it larger. */
/* Animation shown when hovering over the text. */
@keyframes rainbow-text-simple-animation {
    0% {
        background-size: 100%;
    }
    80% {
        background-size: 650%;
    }
    100% {
        background-size: 650%;
    }
}

.custom-menu-item{
    cursor: pointer;
}

.fireworks{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    margin: 0;
}
</style>
<template>
    <div>
        <canvas class="fireworks"></canvas>
        <v-card v-if="!lookingForWinner" class="mx-auto my-12" max-width="1180" :loading="searching" :disabled="searching" ref="form" style="background: transparent !important; box-shadow: none;">
            <template slot="progress">
                <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>
            <v-card-title>
                <v-row
                    no-gutters
                >
                    <v-col
                        cols="12"
                        sm="10"
                        md="10"
                    >
                        <h1 class="gradient-text" v-if="followersCount">{{ followersCount }} Followers for {{searcheduser}}</h1>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="2"
                        md="2"
                        style="width: 100%;"
                    >
                        <v-menu offset-y>
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn
                                    color="primary"
                                    dark
                                    v-bind="attrs"
                                    v-on="on"
                                    class="custom-btn"
                                    style="width:100%"
                                >
                                    Actions
                                </v-btn>
                            </template>
                            <v-list style="padding:0">
                                <v-list-item class="custom-menu-item" style="padding:2px 10px" @click="lookWinner()">
                                    <v-list-item-title>Random Winner</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                    </v-col>
                </v-row>
                
            </v-card-title>
            
            <v-text-field
                :value="itemsPerPage"
                label="Items per page"
                type="number"
                min="1"
                max="50"
                @input="itemsPerPage = parseInt($event, 10)"
                style="padding: 16px;"
            ></v-text-field>
            <v-data-table :headers="headers" 
                :items="followers" 
                :items-per-page="itemsPerPage" 
                :page.sync="page"
                class="elevation-2" 
                @page-count="pageCount = $event"
                hide-default-footer
            >
                <!-- <template v-slot:item.profile_pic_url="{ item }">                    
                    <v-img
                        :lazy-src="item.profile_pic_url"
                        max-height="150"
                        max-width="250"
                        :src="item.profile_pic_url"
                    ></v-img>
                </template> -->
            </v-data-table>
            <div class="text-center pt-2">
                <v-pagination
                  v-model="page"
                  :length="pageCount"
                ></v-pagination>
              </div>
        </v-card>
        <v-card v-if="lookingForWinner && !winnerIsFound" max-width="550" style="margin:0 auto; background:transparent; box-shadow: none;
            margin: 0px auto;
            border: 6px solid #f4f4f4;
            background: #f4f4f4;
            padding: 40px;">
            <div style="height:50%">
                <lottie :options="animationSettings" v-on:animCreated="handleAnimation"/>
            </div>
            <h1 style="text-align:center; bottom:20px; font-size: 33px; font-weight: lighter; color: #333;">Looking for Winner</h1>
        </v-card>
        <h1 v-if="winnerIsFound" class="mx-auto my-12 gradient-text" style="max-width:500">The Winner is ...</h1>
        <v-card
            class="mx-auto my-12"
            max-width="500"
            v-if="winnerIsFound"
        >
            <template slot="progress">
            <v-progress-linear
                color="deep-purple"
                height="10"
                indeterminate
            ></v-progress-linear>
            </template>

            <v-img
                height="250"
                :src="winner.profile_pic_url"
            ></v-img>

            <v-card-title> {{winner.username}}</v-card-title>

            <v-divider class="mx-4"></v-divider>

            <v-card-title>Congratulations for our winner 🔥🔥🔥</v-card-title>

            <v-card-text>
                <div class="my-4 subtitle-1">
                    {{winner.full_name}}
                </div>

                <div>{{winner.userid}}</div>
            </v-card-text>
            
            <v-card-text>
            </v-card-text>

            <v-card-actions>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
    import Lottie from 'vue-lottie';
    import * as animationData from '../animations/29435-random-things.json';

    export default {
        data: function () {
            return {
                    animationSettings: {animationData: animationData,
                },
                searching: false,
                followers: [],
                headers: [
                    { text: 'User Id', value: 'userid' },
                    { text: 'User Name', value: 'username' },
                    { text: 'Full Name', value: 'full_name' },
                    { text: 'Follower For', value: 'follower_for' },
                    // { text: 'Profile Picture', value: 'profile_pic_url' },
                ],
                batchId: null,
                pageCount: 10,
                page: 1,
                itemsPerPage: 10,
                followersCount: 0,
                searcheduser:null,
                lookingForWinner: false,
                winnerIsFound: false,
                winner: {
                    profile_pic_url: null,
                    username: null,
                    full_name: null,
                    userid: null
                }
            }
        },components: {
            'lottie': Lottie
        },
        computed: {
        },
        methods: {
            lookWinner() {
                let self = this;
                this.lookingForWinner = true;
                axios({
                    method: 'get',
                    url: '/followers/batches/' + this.batchId + '/random',
                    data: {}
                }).then((response) => {
                    setTimeout(function(){
                        this.anim.playSegments([0, 120], false);
                        this.anim.addEventListener('loopComplete', function(){
                            let data = response.data;
                            this.winnerIsFound = true;
                            this.winner.profile_pic_url = data.winner.profile_pic_url;
                            this.winner.username = data.winner.username;
                            this.winner.full_name = data.winner.full_name;
                            this.winner.userid = data.winner.userid;
                        }.bind(this));
                    }.bind(this),10000);

                }, (error) => {
                    console.log(error);
                });

            },
            handleAnimation(anim) {
                this.anim = anim;
                this.anim.playSegments([0, 60], true);
            }
        },
        created() {
            let self = this;
            this.batchId = this.$route.params.batchId;
            this.searching = true;
            axios({
                method: 'get',
                url: '/followers/batches/' + this.batchId,
                data: {
                }
            }).then((response) => {
                let batchId = response.data.batch_id;
                console.log(response.data);
                self.followers = response.data.followers;
                self.followersCount = response.data.followers_count;
                if(response.data.followers_count){
                    self.searcheduser = response.data.followers[0].follower_for;
                }
                self.searching = false
            }, (error) => {
                console.log(error);
            });

        },
        updated (){
        }
    };
</script>
<style scoped>
    .v-application .custom-btn {
        background: #ea317c !important;
        padding: 0px 27px;
        height: 38px;
        font-size: 14px;
        min-width: 64px;
    }
    @media only screen and (max-width: 600px) {
        .v-application .custom-btn {
            margin: 27px 0;
        }
    }
</style>