<template>
  <div>
    <v-overlay :value="searching">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>
    <v-card class="mx-auto"   elevation="2" outlined style="margin-top: 20px;" tile>
        <v-list-item-group
            active-class="none"
        >
        <v-list-item v-if="!batches.length" @click="goToSearchFollower()">
            <v-list-item-content>
            <v-list-item-title style="font-weight: bolder; margin-bottom:15px">Currently there are no batches</v-list-item-title>
            <v-list-item-subtitle>Use search followers to create a new batch </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>
        <v-list-item v-for="item in batches" :key="item.id" two-line @click="openBatch(item.id)">
            <v-list-item-content>
            <v-list-item-title style="font-weight: bolder; margin-bottom:15px">Batch {{ item.id }} 
                <v-chip
                    close-icon="mdi-close-outline"
                    :color="getColor(item.status)"
                    label
                    style="color:white !important; margin: 0 13px; padding: 5px 27px;"
                >{{ getLabel(item.status)}}</v-chip>
                <v-btn
                    depressed
                    color="error"
                    v-if="item.status == 'WORKING'"
                    @click.stop="dialogContext = item.id; dialog=true;"
                    v-on:blur.stop=""
                >
                    Stop this batch
                </v-btn>
            </v-list-item-title>
            <v-list-item-subtitle>User {{ item.user }} - {{ item.created_at }} </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-card>
    <v-dialog
            v-model="dialog"
            width="500"
    >
        <v-card>
            <v-card-title class="headline">
                Stop Confirmation
            </v-card-title>

            <v-card-text style="color:#333; padding: 10px;">
                Are you really sure you want to stop this batch.
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="secondary"
                    text
                    @click="dialog = false"
                >
                    Discard
                </v-btn>
                <v-btn
                    color="red"
                    style="color:white"
                    @click="stopBatch(dialogContext)"
                >
                    Stop
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
  </div>
</template>

<script>
    module.exports = {
        data: function () {
            return {
                batches: [],
                overlay: false,
                dialog: false
            };
        },
        methods:{
            goToSearchFollower(){
                this.$router.push({ name: 'Followers'});
            },
            openBatch(batchId){
                this.$router.push({ name: 'FollowersBatch', params: { batchId } })
            },
            stopBatch(batchId){
                let self = this;
                this.searching = true;
                axios({
                    method: 'post',
                    url: '/followers/batches/' + batchId + '/stop',
                    data: {}
                }).then((response) => {
                    //set batch status as failed
                   this.searching = false;
                   this.batches = _.map(this.batches, function(batch){
                       if(batch.id == batchId){
                           batch.status = "FAILED"
                       }
                       return batch;
                   })
                }, (error) => {
                    this.searching = false;
                })
                this.dialog = false;
            },
            getColor(status){
                if(status == "WORKING"){
                    return "blue";
                }else if(status == "COMPLETED"){
                    return "green";
                } else if(status == "DISPATCHED"){
                    return "yellow";
                } else{
                    return "red";
                }
            },
            getLabel(status){
                if(status == "WORKING"){
                    return "Working";
                }else if(status == "COMPLETED"){
                    return "Completed";
                }else if(status == "DISPATCHED"){
                    return "Waiting For Worker";
                }
                else{
                    return "Failed";
                }
            }
        },
        created() {
            let self = this;
            this.searching = true;
            axios({
                method: 'get',
                url: '/followers/batches/',
                data: {
                }
            }).then((response) => {
                self.batches = response.data.batches;
                this.searching = false;
            }, (error) => {
                console.log(error);
                this.searching = false;
            })
        },
    };
</script>

<style scoped>
p {
  font-size: 2em;
  text-align: center;
}
</style>