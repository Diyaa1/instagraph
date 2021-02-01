<template>
  <div>
    <v-banner
        elevation="2"
        single-line
        sticky
    >
      Welcome to instagraph dashboard
    </v-banner>
    <v-card class="mx-auto" elevation="2" style="margin-top: 20px;" tile>
        <v-list-item-group
            active-class="none"
        >
        <v-list-item v-for="item in batches" :key="item.id" two-line @click="openBatch(item.id)">
            <v-list-item-content>
            <v-list-item-title style="font-weight: bolder; margin-bottom:15px">Batch {{ item.id }} <v-chip
                close-icon="mdi-close-outline"
                :color="getColor(item.status)"
                label
                style="color:white !important; margin: 0 13px; padding: 5px 27px;"
            >{{ getLabel(item.status)}}</v-chip></v-list-item-title>
            <v-list-item-subtitle>User {{ item.user }} - {{ item.created_at }} </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-card>
  </div>
</template>

<script>
    module.exports = {
        data: function () {
            return {
                batches: []
            };
        },
        methods:{
            openBatch(batchId){
                this.$router.push({ name: 'FollowersBatch', params: { batchId } })
            },
            getColor(status){
                if(status == "WORKING"){
                    return "blue";
                }else if(status == "COMPLETED"){
                    return "green";
                }
                else{
                    return "red";
                }
            },
            getLabel(status){
                if(status == "WORKING"){
                    return "Working";
                }else if(status == "COMPLETED"){
                    return "Completed";
                }
                else{
                    return "Failed";
                }
            }
        },
        created() {
            let self = this;
            this.batchId = this.$route.params.batchId;
            this.searching = true;
            axios({
                method: 'get',
                url: '/followers/batches/',
                data: {
                }
            }).then((response) => {
                self.batches = response.data.batches;
            }, (error) => {
                console.log(error);
            });
        },
    };
</script>

<style scoped>
p {
  font-size: 2em;
  text-align: center;
}
</style>