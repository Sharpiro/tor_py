<template>
  <div>
    <h1>{{ msg }}</h1>
    <div class="card-holder" v-for="item in groceryList" v-bind:key="item.id">
      <component :is="item.cardType" v-bind:item="item" />
    </div>
  </div>
</template>

<script>
import Card from "./Card.vue";
import Create2Card from "./Create2Card.vue";


export default {
  props: {
    msg: String
  },
  components: {
    Card,
    Create2Card
  },
  data() {
    return {
      cardType: "Card",
      groceryList: [
        {
          id: 0,
          cardType: "Card",
          type: "sendVersions",
          text: "Send Versions",
          showRaw: false,
          rawData: new Array(100).fill(0)
        },
        {
          id: 1,
          cardType: "Card",
          type: "receiveVersions",
          text: "Receive Versions",
          showRaw: false,
          rawData: new Array(100).fill(1)
        },
        {
          id: 2,
          cardType: "Card",
          type: "receiveCerts",
          text: "Receive Certs",
          showRaw: false,
          rawData: new Array(100).fill(2)
        },
        {
          id: 3,
          cardType: "Create2Card",
          type: "receiveNetInfo",
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
