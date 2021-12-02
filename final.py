class Node: ## class for creating node objects
    def __init__(self,battery=100,data=100):
        self.battery=battery
        self.data=data
    def set_values(self,battery=100,data=100):
        self.battery=battery
        self.data=data
    def get_values(self):
        return self.battery, self.data

class Gateway:  ## class for creating gateway objects
    def __init__(self,power=100,storage=100):
        self.power=power
        self.storage = storage
    def set_values(self,power,storage):
        self.storage=storage
        self.power=power
    def get_values(self):
        return self.power,self.storage

class Graph:	## class for creating graph objects
    def __init__(self,num_of_nodes,num_of_gateways):
        self.rows=num_of_nodes
        self.cols=num_of_gateways
        self.adjmatrix=[]
        for i in range(self.rows):
            self.adjmatrix.append([0 for j in range(self.cols)])
    def set_values(self,row,col,value):
        self.adjmatrix[row][col]=value
    def print_graph(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.adjmatrix[i][j],end=" ")
            print('\n')
        print('\n')

def create_nodes(): ## function to create nodes
    while True:
        try:
            n = int(input("Enter number of nodes: "))
        except ValueError:
                print("Invalid input, try again")
                continue
        if n<=0:
            print("Number of nodes cannot be negative & zero ")
            continue
        else:
            break
    nodes = [Node() for i in range(n)]
    for i in range(n):
        #battery = int(input("Enter the battery in node{}: ".format(i)))
        data = int(input("Enter the data in node{}: ".format(i)))
        nodes[i].set_values(data,data)
    return nodes

def create_gateways(): ## function to create gateways
    while True:
        try:
            g = int(input("Enter number of gateways: "))
        except ValueError:
            print("Invalid input, try again")
            continue
        if(g<=0):
            print("Number of gateways cannot be negative & zero ")
            continue
        else:
            break
    gateways = [Gateway() for i in range(g)]
    for i in range(g):
        while True:
            try:
                power = int(input("Enter the power in gateway{}: ".format(i)))
            except ValueError:
                print("Invalid input, try again")
                continue
            if(power<0):
                print("Power cannot be negative ")
                continue
            else:
                break
        while True:
            try:
                storage = int(input("Enter the storage in gateway{}: ".format(i)))
            except ValueError:
                print("Invalid input, try again")
                continue
            if(storage<0):
                print("Storage cannot be negative ")
                continue
            else:
                break
        gateways[i].set_values(power,storage)
    return gateways

def create_graph(num_of_nodes,num_of_gateways):
    graph = Graph(num_of_nodes,num_of_gateways)
    for i in range(num_of_nodes):
        for j in range(num_of_gateways):
            while True:
                try:
                    graph.set_values(i,j,int(input("Enter if there is an edge b/w node {} to gateway {}: ".format(i,j))))
                except ValueError:
                    print("Invalid input, try again")
                    continue
                if(graph.adjmatrix[i][j]<0):
                    print("Value cannot be negative ")
                    continue
                elif(graph.adjmatrix[i][j]>1):
                    print("Value cannot be greater than 1 ")
                    continue
                else:
                    break
    return graph

def gateways_connected_to_nodes(nodes,gateways,matrix):
    gateways_connected_to_nodes_list={}
    for i in range(len(nodes)):
        for j in range(len(gateways)):
            if(matrix.adjmatrix[i][j]==1):
                if(i in gateways_connected_to_nodes_list):
                    gateways_connected_to_nodes_list[i].append(j)
                else:
                    gateways_connected_to_nodes_list[i]=[j]
    return gateways_connected_to_nodes_list

def calculate_the_cost(each_node,each_gateway,nodes,gateways,matrix):
    cost=0
    ratio=float('inf')
    if(each_node.data>0):
        ratio = each_gateway.power/each_node.data
    return ratio

def TotalData(nodes): ## function to calculate the total data
    total_data=0
    for i in range(len(nodes)):
        total_data+=nodes[i].data
    return total_data

def TotalStorage(gateways): ## function to calculate the total power
    total_storage=0
    for i in range(len(gateways)):
        total_storage+=gateways[i].storage
    return total_storage

def optimization(nodes,gateways,matrix):
    print("Optimization started")
    ratio={}
    mini_ratio = float('inf')
    final_gateways=[]
    gateways_connected_to_nodes_list=gateways_connected_to_nodes(nodes,gateways,matrix)
    while TotalData(nodes)>0 and TotalStorage(gateways)>0:
        for i in range(len(nodes)):
            for j in range(len(gateways)):
                if(matrix.adjmatrix[i][j]==1):
                    ratio[(i,j)]=calculate_the_cost(nodes[i],gateways[j],nodes,gateways,matrix)
        for i in range(len(nodes)):
            for j in range(len(gateways)):
                if(matrix.adjmatrix[i][j]==1):
                    if(ratio[(i,j)]<mini_ratio):
                        mini_ratio=ratio[(i,j)]
                        mini_node=i
                        mini_gateway=j
        if(mini_ratio==float('inf')):
            print("Optimization complete")
            return
        else:
            print("Optimization in progress")
            final_gateways.append(mini_gateway)
            print("Node {} is connected to gateway {} with ratio {}".format(mini_node,mini_gateway,mini_ratio))
            data_to_be_sent=min(nodes[mini_node].data, gateways[mini_gateway].storage)
            nodes[mini_node].data-=data_to_be_sent
            gateways[mini_gateway].storage-=data_to_be_sent
            matrix.adjmatrix[mini_node][mini_gateway]=0
            mini_ratio=float('inf')
    print("Optimization complete")
    print(final_gateways)
    


    


if __name__ == '__main__':
    nodes = create_nodes()
    gateways = create_gateways()
    graph = create_graph(len(nodes),len(gateways))
    graph.print_graph()
    for i in range(len(nodes)):
        print("Data in node{}: {}".format(i,nodes[i].get_values()))

    print("\n")
    for i in range(len(gateways)):
        print("Power in gateway{}: {}".format(i,gateways[i].get_values()[0]))
        print("Storage in gateway{}: {}".format(i,gateways[i].get_values()[1]))

    print("\n")
    print(optimization(nodes,gateways,graph))

