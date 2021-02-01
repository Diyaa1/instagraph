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
</style>
<template>
    <div>
        <v-card class="mx-auto my-12" max-width="1180" :loading="searching" :disabled="searching" ref="form" style="background: transparent !important; box-shadow: none;">
            <template slot="progress">
                <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>
            <v-card-title><h1 class="gradient-text" v-if="followersCount">{{ followersCount }} Followers for {{searcheduser}}</h1></v-card-title>
            
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
    </div>
</template>

<script>
    module.exports = {
        data: function () {
            return {
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
                searcheduser:null
            }
        },
        computed: {
        },
        methods: {
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
    };
</script>