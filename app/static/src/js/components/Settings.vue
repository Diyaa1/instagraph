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
            <v-card-title>Settings</v-card-title>
            <v-card-text>
                <form>
                <v-col cols="12" md="12">
                    <v-text-field 
                        ref="loginName"
                        v-model="loginName"  
                        :rules="[rules.required]"
                        label="Required" 
                        required
                    ></v-text-field>
                </v-col>    

                <v-col cols="12" md="12">
                    <v-text-field
                        ref="password"
                        v-model="password"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[rules.required]"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        label="Required"
                        @click:append="show1 = !show1"
                ></v-text-field>
                </v-col>

                    <v-btn
                        class="mr-4"
                        @click="dialog = true"
                    >
                        Save
                    </v-btn>
                </form>
            </v-card-text>
        </v-card>
        <v-dialog
            v-model="dialog"
            width="500"
        >
            <v-card>
                <v-card-title class="headline">
                    Change Confirmation
                </v-card-title>

                <v-card-text style="color:#333; padding: 10px;">
                    Are you really sure you want to save these changes.
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
                        @click="save()"
                    >
                        Save Changes
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
                password: null,
                loginName: null,
                show1: false,
                loading: false,
                dialog: false,
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
                    loginName: this.loginName,
                    password: this.password,
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
                    url: '/admin/settings',
                    data: {
                        loginName: this.loginName,
                        password: this.password
                    }
                }).then((response) => {
                    this.$router.push({ name: 'Index' })
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
                    url: '/admin/settings',
                    data: {
                    }
                }).then((response) => {
                    let data = response.data;
                    this.password = data.PASSWORD;
                    this.loginName = data.USER;
                    this.loading = false;
                }, (error) => {
                    console.log(error);
                    this.loading = false;
                })
        },
    };
</script>

<style scoped>
</style>