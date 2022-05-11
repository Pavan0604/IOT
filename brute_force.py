import itertools
from platform import node
from typing import final

from major import calculate_the_cost
class Node:
    def __init__(self):
        self.data = 0
        self.battery = 0
    def set_values(self,data,battery):
        self.data = data
        self.battery = battery
    def get_data(self):
        return self.data
    def get_battery(self):
        return self.battery

class Gateway:
    def __init__(self):
        self.power = 0
        self.storage = 0
    def set_values(self,power,storage):
        self.power = power
        self.storage = storage
    def get_power(self):
        return self.power
    def get_storage(self):
        return self.storage

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
            if(matrix.adjmatrix[i][j]==1 and gateways[j].storage>0):
                if(i in gateways_connected_to_nodes_list):
                    gateways_connected_to_nodes_list[i].append(j)
                else:
                    gateways_connected_to_nodes_list[i]=[j]
    return gateways_connected_to_nodes_list

def check_storage(val,gateways):
    arr = []
    for i in val:
        if(gateways[i].get_storage()>0):
            arr.append(i)
    return arr


def TotalStorage(gateways): ## function to calculate the total power
    total_storage=0
    for i in range(len(gateways)):
        total_storage+=gateways[i].storage
    return total_storage

def TotalData(nodes): ## function to calculate the total data
    total_data=0
    for i in range(len(nodes)):
        total_data+=nodes[i].data
    return total_data

def FindCombinations(values):
    combinations = []
    for L in range(0,len(values)+1):
        for subset in itertools.combinations(values, L):
            if(len(subset)>1):
                combinations.append(list(subset))
    return combinations


def FindRatio(node_val,combinations,gateways,nodes):
    cost = {}
    ratio = float("inf")
    print(combinations)
    for i in range(len(combinations)):
        total = 0
        print(combinations[i])
        for j in combinations[i]:
            total += gateways[j].power
        if(nodes[node_val].data>=1): ## if data is greater than 1   
            ratio = total/nodes[node_val].data
            temp = tuple(combinations[i])
            cost[temp] = ratio
    return cost
            

def brute_force(nodes,gateways,matrix):
    final_gateways = []
    intial_storage = TotalStorage(gateways)
    intial_data = TotalData(nodes) 
    total_storage = TotalStorage(gateways)
    total_data = TotalData(nodes)
    while(total_storage>0 and total_data>0):
        gateways_connected_to_nodes_list = gateways_connected_to_nodes(nodes,gateways,matrix)
        print(gateways_connected_to_nodes_list)
        find_all_combinations = {}
        for key, values in gateways_connected_to_nodes_list.items():
            find_all_combinations[key] = FindCombinations(values)

        print(find_all_combinations)
        calculate_the_cost = {}
        for key, vals in find_all_combinations.items(): 
            calculate_the_cost[key] = FindRatio(key,vals,gateways,nodes)
        print(calculate_the_cost)

        minimum = float('inf')
        for key, vals in calculate_the_cost.items():
            for key1, vals1 in vals.items():
                if(vals1<minimum):
                    minimum = vals1
                    gate_selected = key1
                    node_selected = key
        print(node_selected,gate_selected,minimum)  

        if(minimum!=float('inf')):
            for i in gate_selected:
                if(gateways[i].get_storage()>=nodes[node_selected].data):
                    data_transferred = nodes[node_selected].data
                    gateways[i].storage -= data_transferred
                    nodes[node_selected].data = 0
                else:
                    if(nodes[node_selected].data>0):
                        data_transferred = gateways[i].storage
                        gateways[i].storage = 0
                        nodes[node_selected].data -= data_transferred
            final_gateways.append(gate_selected)
            total_storage -= data_transferred
            total_data -=  data_transferred
        else:
            print("No more combinations")
            break
    final_storage = TotalStorage(gateways)
    final_data = TotalData(nodes)
    total_power_consumed = intial_storage - final_storage
    total_data_transferred = final_data - intial_data
    print("Total power consumed: ",total_power_consumed)

    print(final_gateways)
        

if __name__ == "__main__":
    nodes = create_nodes()
    gateways = create_gateways()
    matrix = create_graph(len(nodes),len(gateways))
    #print(nodes)
    #print(gateways)
    #print(matrix.adjmatrix)
    brute_force(nodes,gateways,matrix)
    
