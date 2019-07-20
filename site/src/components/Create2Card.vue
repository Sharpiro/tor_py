<template>
  <div class="card">
    <div class="container">
      <div>
        <b>A whole new card2</b>
      </div>
      <div>
        with some custom data here
      </div>
      <button v-on:click="toggle">Toggle</button>
      <p v-if="this.item.showRaw">{{item.rawData}}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    item: Object
  },
  data() {
    return {};
  },
  methods: {
    toggle: function() {
      this.item.showRaw = !this.item.showRaw;
      console.log(this.item.showRaw);
    }
  }
};
</script>

<style scoped>
.card {
  word-wrap: break-word;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 100%;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

.container {
  padding: 10px 10px 10px 10px;
}
</style>
