const net = require("net");

const client = net.createConnection("./unix.sock"); 
client.on("connect", () => {
    console.log("connected to the server")
});
client.on("data", () => {
    console.log(data)
});
client.on("end", () => {
    console.log("Disconnected")
    client.destroy()
})
client.on("close", () => {
    console.log("Closing")
})
client.on("error", (err) => {
    console.error(err.message);
})

let id = 0;

console.log("")
method = prompt("Input the method you want to do :")
params = prompt("Input the params")
client.write(
    {
        "method": method,
        "params": params,
        "params_type": params.forEach(ele => typeof ele),
        "id": id,
    }
);

