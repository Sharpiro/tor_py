<template>
  <div id="app">
    <Main msg="Tor-Py" />
  </div>
</template>

<script>
import Main from "./components/Main.vue";

export default {
  components: {
    Main
  }
};
</script>

<style>
#app {
  width: 50%;
  margin: auto;
}
</style>
