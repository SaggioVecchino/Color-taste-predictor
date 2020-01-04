import Datastore from "nedb";

var colors = new Datastore({
  filename: "./colors.db",
  timestampData: true,
  autoload: true,
  inMemoryOnly: false,
  timestampData: false
});

export default colors;
