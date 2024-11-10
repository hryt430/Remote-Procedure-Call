import socket
import math
import os
import json

def floor(x):
    return math.floor(x)

def nroot(n, x):
    return math.pow(x,1/n)

def reverse(s):
    return s[::-1]

def validAnagram(s1, s2):
    return sorted(s1) == sorted(s2)

def sort(strArr):
    return sorted(strArr)

functions = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": validAnagram,
    "sort": sort
}

class Socket:
    def __init__(self, server_address):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_address = server_address
    
    def bind_serverAdress(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass

        print("Connecting to {}".format(self.server_address))

        # self.sock.bind(self.server_address)

        # self.sock.listen(1)
        try:
            self.sock.bind(self.server_address)
            self.sock.listen(1)
            print("Server is listening on {}".format(self.server_address))
        except Exception as e:
            print(f"Error binding or listening: {e}")
            raise
    def process_request(self):
        while True:
            connection, client_adress = self.sock.accept()
            try:
                print("connection to client side")
                while True:
                    data = connection.recv(4096)

                    if not data:
                        print("no data !")
                        break
                        
                    data_str = data.decode("utf-8")

                    print("Received" + data_str)

                    request_data = json.loads(data_str)
                    method = request_data["method"]
                    params = request_data["params"]
                    id = request_data["id"]

                    response = Response(method, params)
                    try:
                        if(response.isValidParams() and functions.get(method)):
                            results, result_type = response.processData()
                        else:
                            if(not response.isValidParams()):
                                message = response.Errors["invalidParams"]
                            else:
                                message = response.Errors["invalidMethod"]
                            print(message)
                            connection.sendall(json.dumps(message).encode())
                            continue

                    except Exception as e:
                        message = f"Error while processing data: {e}"
                        print(message)
                        connection.sendall(json.dumps(message).encode())

                    answer = {
                                "results": results,
                                "result_type": result_type,
                                "id": id
                            }
                    
                    print(answer)
                    connection.sendall(json.dumps(answer).encode())

            except Exception as e:
                message = f"Error while connectiong to the client: {e} "
                print(message)
                connection.sendall(json.dumps(message).encode())
            
            finally:
                print("closing socket")
                self.sock.close()     
                break  

class Response:
    def __init__(self, method, params):
        self.method = method
        self.params = params
        self.Errors = {
                        "invalidParams": "Error invalid params!" ,
                        "invalidMethod": "Error method not found!",
                      }

    def isValidParams(self):
        if self.method == "floor":
            return type(self.params[0]) == float
        
        elif self.method == "nroot":
            return all(type(param) == int for param in self.params) and len(self.params) == 2
        
        elif self.method == "reverse":
            return type(self.params[0]) == str
        
        elif self.method == "validAnagram":
            return all(type(param) == str for param in self.params) and len(self.params) == 2
        
        elif self.method == "sort":
            return all(type(param) == str for param in self.params)

    def processData(self):
        if self.method == "floor":
            return functions[self.method](self.params[0]), "int"
        
        elif self.method == "nroot":
            return functions[self.method](self.params[0], self.params[1]), "float"
        
        elif self.method == "reverse":
            return functions[self.method](self.params[0]), "str"
        
        elif self.method == "validAnagram":
            return functions[self.method](self.params[0], self.params[1]), "bool"
        
        elif self.method == "sort":
            return functions[self.method](self.params), "str[]"
    
def main():
    sock = Socket("./unix.sock")
    sock.bind_serverAdress()
    sock.process_request()

if __name__ == "__main__":
    main()