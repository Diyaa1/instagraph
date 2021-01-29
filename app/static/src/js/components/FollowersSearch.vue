<template>
    <v-card class="mx-auto my-12" max-width="600" :loading="searching" :disabled="searching" ref="form">
        <template slot="progress">
            <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
        </template>

        <v-img height="250" src="/images/instagram.png"></v-img>

        <v-card-title>Search Form</v-card-title>

        <v-card-text>
            <v-row>
                <v-col cols="12" md="6">
                    <v-text-field 
                        ref="loginName"
                        v-model="loginName"  
                        :rules="[rules.required]"
                        label="Login Name" 
                        required
                    ></v-text-field>
                </v-col>    

                <v-col cols="12" md="6">
                    <v-text-field
                        ref="password"
                        v-model="password"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[rules.required]"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        label="Password"
                        @click:append="show1 = !show1"
                  ></v-text-field>
                </v-col>

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
                searching:false,
                rules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                    emailMatch: () => (`The email and password you entered don't match`),
                },
            }
        },
        computed: {
            form() {
                return {
                    loginName: this.loginName,
                    password: this.password,
                    searchUser: this.searchUser,
                }
            },
        },
        methods: {
            search: function () {
                this.formHasErrors = false

                Object.keys(this.form).forEach(f => {
                if (!this.form[f]) 
                    this.formHasErrors = true
                    this.$refs[f].validate(true)
                })

                if(this.formHasErrors){
                    return;
                }

                this.searching = true;

                
            }

            
        }
    };
</script>