<template>
  <div id="app">
    <h1>My color taste predictor</h1>
    <Color />
  </div>
</template>

<script>
import Color from "@/components/Color.vue";

export default {
  name: "App",
  components: {
    Color
  }
};
</script>

<style>
html,
body,
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

h1 {
  font-family: "PT Sans", sans-serif;
  margin-bottom: 2px;
}

#app {
  text-align: center;
}

* {
  font-family: "Open Sans", sans-serif;
  size: 22px;
}
</style>
