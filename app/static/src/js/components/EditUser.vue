<template>
    <div>
        <v-card
            elevation="2"
            max-width="600"
            class="mx-auto my-12"
            :loading="loading"
            :disabled="loading"
        >
            <template slot="progress">
                <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>
            <v-card-title>Edit User</v-card-title>
            <v-card-text>
                <form>
                <v-col cols="12" md="12">
                    <v-text-field 
                        ref="username"
                        v-model="username"  
                        :rules="[rules.required]"
                        label="User Name" 
                        required
                    ></v-text-field>
                    <v-text-field
                        v-model="password"
                        ref="password"
                        label="Password (Fill this if you want to update password)"
                    ></v-text-field>
                </v-col>    
                </v-col>
                    <v-btn
                        class="mr-4"
                        @click="save()"
                    >
                        Save
                    </v-btn>
                </form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
    module.exports = {
        data: function () {
            return {
                username: null,
                password: null,
                loading: false,
                rules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                    emailMatch: () => (`The email and password you entered don't match`),
                },
            };
        },
        computed: {
            form() {
                return {
                    username: this.username
                }
            },
        },
        methods:{
            save: function () {
                this.formHasErrors = false;

                Object.keys(this.form).forEach(f => {
                if (!this.form[f]) 
                    this.formHasErrors = true
                    this.$refs[f].validate(true)
                })

                if(this.formHasErrors){
                    return;
                }

                this.loading = true;

                axios({
                    method: 'post',
                    url: '/admin/users/' + this.$route.params.userId,
                    data: {
                        username: this.username,
                        password: this.password
                    }
                }).then((response) => {
                    this.$router.push({ name: 'UsersList' })
                    this.loading = false;
                }, (error) => {
                    console.log(error);
                    this.loading = false;
                })

            },
        },
        created() {
            let self = this;
            this.loading = true;
            axios({
                    method: 'get',
                    url: '/admin/users/' + this.$route.params.userId,
                    data: {
                    }
                }).then((response) => {
                    let data = response.data;
                    this.loading = false;
                    this.username = response.data.username;
                }, (error) => {
                    console.log(error);
                    this.loading = false;
                })
        },
    };
</script>

<style scoped>
</style>