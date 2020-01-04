import Datastore from "nedb";

var persist = new Datastore({
    filename: "./persist.db",
    timestampData: false,
    autoload: true,
    inMemoryOnly: false,
    timestampData: false
});

export default persist;