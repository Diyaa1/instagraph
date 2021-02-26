<template>
  <div>
    <v-card class="mx-auto my-12" max-width="1180" :loading="searching" :disabled="searching" ref="form" style="background: transparent !important; box-shadow: none;">
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
                    Create User
                </v-col>
                <v-col
                    cols="12"
                    sm="2"
                    md="2"
                    style="text-align: right"
                >
                    <v-btn
                        class="ml-4 px-8"
                        width="200px"
                        color="primary"
                        @click="$router.push({ name: 'CreateUser'})"
                    >
                        Create
                    </v-btn>
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
            :items="users" 
            :items-per-page="itemsPerPage" 
            :page.sync="page"
            class="elevation-2" 
            @page-count="pageCount = $event"
            hide-default-footer
        >
            <template v-slot:item.roles="{ item }">
                <v-chip v-for="(role, index) in item.roles" :key ="index"
                    :color="getColor(role)"
                    dark
                    label
                    class="mx-1"
                >
                    {{ role }}
                </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    depressed
                    color="primary"
                    @click="$router.push({ name: 'EditUser', params: { userId: item.id }})"
                >
                    Edit
                </v-btn>
                <v-btn
                    depressed
                    color="error"
                    @click="dialog = true; dialogContext = item;"
                >
                    Delete
                </v-btn>
            </template>
        </v-data-table>
        <div class="text-center pt-2">
            <v-pagination
                v-model="page"
                :length="pageCount"
            ></v-pagination>
        </div>
    </v-card>  
    <v-dialog
            v-model="dialog"
            width="500"
    >
        <v-card>
            <v-card-title class="headline">
                Delete Confirmation
            </v-card-title>

            <v-card-text style="color:#333; padding: 10px;">
                Are you really sure you want to delete this user.
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
                    @click="deleteUser(dialogContext)"
                >
                    Delete
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
                searching: false,
                dialog: false,
                dialogContext: null,
                users: [],
                headers: [
                    { text: 'User Id', value: 'id' },
                    { text: 'User Name', value: 'username' },
                    { text: 'Roles', value: 'roles' },
                    { text: 'Actions', value: 'actions' },
                ],
                pageCount: 10,
                page: 1,
                itemsPerPage: 10,
            }
        },
        methods:{
            getColor(role){
                if(role == "superadmin"){
                    return "deep-purple accent-4"
                }
                if(role == "admin"){
                    return "orange"
                }
            },
            deleteUser(user){
                this.searching = true;
                axios({
                    method: 'delete',
                    url: '/admin/users/' + user.id,
                }).then((response) => {
                    this.dialog = false;
                    this.searching = false;
                    this.users = _.filter(this.users, function(item) {
                        return item.id != user.id;
                    });
                }, (error) => {
                    console.log(error);
                });
            }
        },
        created() {
            this.searching = true;
            axios({
                method: 'get',
                url: '/admin/users',
            }).then((response) => {
               this.users = response.data;
               this.searching = false;
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