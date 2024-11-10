const net = require("net");
const readline = require("readline")

const server_address = "./unix.sock";
let id = 0

function readInput(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    
    return new Promise(resolve => {
        rl.question(question, answer => {
            rl.close();
            resolve(answer);
        });
    });
};

async function connectToServer(address) {
    
    console.log("Connecting to the server");

    return new Promise((resolve, reject) => {
        const client = net.createConnection(address, () => {
            console.log("Connected to server");
            resolve(client); 
        });

        client.on("error", (err) => {
            console.error("Connection error:", err);
            reject(err);
        });
    });
};

async function sendToServer(server) {
    try{
        console.log("Sending requests to the server");
        while (true){
        const method = await readInput("Input the method you want to do :");
        const params_input = await readInput("Input the params :");
        const params = method == "floor" || method == "nroot"
                                  ?params_input.split(" ").map(ele => Number(ele))
                                  :params_input.split(" ")

        const request = {
            "method": method,
            "params": params,
            "params_type": params.map(ele => typeof ele),
            "id": id++,
        }

        server.write(JSON.stringify(request));

        const timeout = setTimeout(() => {
            console.log("Timeout ending listenig for server responses");
            server.end();
        }, 2000)

        server.on("data", (data) => {
            if (data) {
                const response = JSON.parse(data)
                console.log("Server response :\n " + JSON.stringify(response));
                clearTimeout(timeout);
                // server.end()
            } 
        })

        server.on("error", (err) => {
            console.error("Server error:", err);
            clearTimeout(timeout);
            server.end();
        });

        server.on("end", () => {
            console.log("Closing connection")
            clearTimeout(timeout)
        })
        }
    }catch(err){
        console.error("Error while sending to server:", err);
    }
};

connectToServer(server_address)
    .then(sendToServer)
    .catch((err) => {
        console.error("Failed to connect to server:", err);
    });

