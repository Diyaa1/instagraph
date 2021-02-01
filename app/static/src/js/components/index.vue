<template>
  <div>
    <v-banner
        elevation="2"
        single-line
        sticky
    >
      Welcome to Followers Picker dashboard
    </v-banner>
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
        },
        created() {
        },
    };
</script>

<style scoped>
p {
  font-size: 2em;
  text-align: center;
}
</style>