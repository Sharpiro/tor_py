<template>
  <div>
    <h1>{{ msg }}</h1>
    <div class="card-holder" v-for="item in groceryList" v-bind:key="item.id">
      <Card v-bind:item="item" />
    </div>
  </div>
</template>

<script>
import Card from "./Card.vue";

export default {
  props: {
    msg: String
  },
  components: {
    Card
  },
  data() {
    return {
      groceryList: [
        {
          id: 0,
          text: "Send Versions",
          showRaw: false,
          rawData: new Array(100).fill(0)
        },
        {
          id: 1,
          text: "Receive Versions",
          showRaw: false,
          rawData: new Array(100).fill(1)
        },
        {
          id: 2,
          text: "Receive Certs",
          showRaw: false,
          rawData: new Array(100).fill(2)
        },
        {
          id: 3,
          text: "Receive NetInfo",
          showRaw: true,
          rawData: new Array(100).fill(3)
        }
      ]
    };
  }
};
</script>

<style scoped>
.card-holder {
  padding: 15px 0 15px 0;
}
</style>
