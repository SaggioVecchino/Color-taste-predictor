<template>
  <div>
    <div class="color" :style="{ background: this.color }"></div>
    <h4>Do I like it?</h4>
    <button @click="likeIt">Yes I do ! (1)</button>
    <button @click="hateIt">No I don't ! (0)</button>
    <button v-if="this.canPredict" @click="predict">Predict (2)</button>
    <button v-if="this.canPredict" @click="reset">Reset!</button>
    <div v-if="this.canPredict">
      <h2>I may like</h2>
      <div class="colors">
        <div
          v-for="item in colorsIMayLike"
          :key="item"
          :style="{ background: item }"
        ></div>
      </div>
      <h2>I may hate</h2>
      <div class="colors">
        <div
          v-for="item in colorsIMayHate"
          :key="item"
          :style="{ background: item }"
        ></div>
      </div>
    </div>
    <div v-else>
      You will be able to predict after giving {{ this.cpt }} appreciation.
    </div>
    <h4>{{ this.console }}</h4>
  </div>
</template>

<script>
import colors from "../assets/DB/colors.js";
import persist from "../assets/DB/persist.js";
import { PythonShell } from "python-shell";
import fs from "fs";
import path from "path";

export default {
  name: "Color",
  data() {
    return {
      R: 0,
      G: 0,
      B: 0,
      colorsIMayLike: [],
      colorsIMayHate: [],
      cpt: 50,
      canPredict: false,
      console: ""
    };
  },
  methods: {
    async likeIt() {
      await this.add(true);
      this.next();
    },
    async hateIt() {
      await this.add(false);
      this.next();
    },
    async add(likeIt) {
      let color = {
        r: this.R,
        g: this.G,
        b: this.B,
        likeIt: likeIt
      };
      await colors.insert(color);
    },
    async next() {
      if (this.cpt > 0 && --this.cpt == 0) this.canPredict = true;
      await persist.update(
        {},
        {
          colorsIMayLike: this.colorsIMayLike,
          colorsIMayHate: this.colorsIMayHate,
          cpt: this.cpt,
          canPredict: this.canPredict
        },
        {}
      );
      this.R = Math.floor(256 * Math.random());
      this.G = Math.floor(256 * Math.random());
      this.B = Math.floor(256 * Math.random());
    },
    async predict() {
      if (!this.canPredict) return;
      var vm = this;
      colors.find({}, async function(e, c) {
        let csvData =
          "r,g,b,likeIt\n" +
          c
            .map(t => t.r + "," + t.g + "," + t.b + "," + (t.likeIt ? 1 : 0))
            .join("\n");
        fs.writeFileSync("colors.csv", csvData, { flag: "w" });

        vm.console = "Predicting...";

        await PythonShell.run(
          "src/renderer/script.py",
          {
            args: ["colors.csv"]
          },
          function(err, results) {
            if (err) {
              vm.console = "Error !";
              throw err;
            }
            vm.console = "Precision: " + results[0];
            vm.colorsIMayLike = JSON.parse(results[1]);
            vm.colorsIMayHate = JSON.parse(results[2]);
          }
        );

        await persist.update(
          {},
          {
            colorsIMayLike: vm.colorsIMayLike,
            colorsIMayHate: vm.colorsIMayHate,
            cpt: vm.cpt,
            canPredict: vm.canPredict
          },
          {}
        );
      });
    },
    async reset() {
      await colors.remove({});
      await persist.remove({});
      this.cpt = 50;
      this.canPredict = false;
      this.console = "";
      this.colorsIMayLike = [];
      this.colorsIMayHate = [];
    }
  },
  computed: {
    color() {
      let rgbToHex = function(rgb) {
        let hex = Number(rgb).toString(16);
        if (hex.length < 2) {
          hex = "0" + hex;
        }
        return hex;
      };
      return "#" + rgbToHex(this.R) + rgbToHex(this.G) + rgbToHex(this.B);
    }
  },
  async mounted() {
    var vm = this;
    await persist.findOne({}, async (e, r) => {
      if (!r) {
        await persist.insert({
          colorsIMayLike: [],
          colorsIMayHate: [],
          cpt: 50,
          canPredict: false
        });
        return;
      } else {
        vm.colorsIMayLike = r.colorsIMayLike;
        vm.colorsIMayHate = r.colorsIMayHate;
        vm.cpt = r.cpt;
        vm.canPredict = r.canPredict;
      }
    });
    window.addEventListener("keyup", async function(event) {
      if (event.key === "1") {
        vm.likeIt();
      } else if (event.key === "0") {
        vm.hateIt();
      } else if (event.key === "2") {
        vm.predict();
      }
    });
    this.R = Math.floor(256 * Math.random());
    this.G = Math.floor(256 * Math.random());
    this.B = Math.floor(256 * Math.random());
  }
};
</script>

<style scoped>
.color {
  width: 300px;
  height: 300px;
  margin: auto;
}

.colors {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.colors div {
  width: 15px;
  height: 15px;
  margin: 2px;
}
</style>
