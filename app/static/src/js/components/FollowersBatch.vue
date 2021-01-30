<template>
    <div>

        <v-card class="mx-auto my-12" max-width="1180" :loading="searching" :disabled="searching" ref="form" style="background: transparent !important; box-shadow: none;">
            <template slot="progress">
                <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>
            <v-card-title>Search Results for batch {{ batchId }}</v-card-title>
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
                <template v-slot:item.profile_pic_url="{ item }">                    
                    <v-img
                        :lazy-src="item.profile_pic_url"
                        max-height="150"
                        max-width="250"
                        :src="item.profile_pic_url"
                    ></v-img>
                </template>
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
                    { text: 'Id', value: 'id' },
                    { text: 'User Name', value: 'username' },
                    { text: 'Full Name', value: 'full_name' },
                    { text: 'Follower For', value: 'follower_for' },
                    { text: 'Profile Picture', value: 'profile_pic_url' },
                ],
                batchId: null,
                pageCount: 10,
                page: 1,
                itemsPerPage: 10
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
                self.followers = response.data.followers
                self.searching = false
            }, (error) => {
                console.log(error);
            });
        },
    };
</script>