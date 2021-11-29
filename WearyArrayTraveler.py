import argparse
import numpy as np
import sys
from colorama import init
from termcolor import colored
import csv
import json
from typing import List
from prettytable import PrettyTable

# Code description: the program gets a file path from the user which contains one or more arrays,
# and prints to the screen a table whether reaching the last element for each array is possible,
# according to the following traversing rules:
# The first index is 0, that’s where the algorithm starts.
# Algorithm may only ‘jump’ forward or backwards in the array according to the 
# value in the ‘current’ element (e.g. if the value at index 0 is 3 the algo may only
# advance to index 3. if the value at index 3 is 2 – the algo may advance to both index 5 and index 1).

#########################################################################################
# !User Attantion!                                                                      #
#########################################################################################
# The file should only be of the folowing formats : CSV, TSV, JSON.                     #
# The file should only contain a single array Or a list of arrays of unsigned integers. #
#########################################################################################

class WearyArrayTraveler:
    def __init__(self):
        pass

    # return the valid successors of a given state in array
    # in concern to a valid step : According to the value in the ‘current’ state,
    # a successor can be (state + value) or (state - value) if those are in the array's boundry.
    def get_successors(self,arr: List[int], state: int) -> List[int]:
        successors = []
        step = arr[state]
        newState1 = state + step
        newState2 = state - step
        if(newState1 < len(arr)):
            successors.append(newState1)
        if(newState2 >= 0):
            successors.append(newState2)
        return successors

    # return True if the aray is traverseable according to the rulse. Otherwise - return False.
    def is_array_traverseable(self, arr: List[int], startState : int = 0, goalState = -1) -> bool:
        goalState = len(arr) - 1 if goalState == -1  else goalState
        frontier = Queue()
        explored = set() # the states that was aleady explored
        frontier.push(startState) # push the first state. Each state is an index in the given array.
        while not frontier.isEmpty():
            state = frontier.pop()
            if state in explored:
                continue
            explored.add(state)
            if state == goalState:
                return True
            successors = self.get_successors(arr, state)
            for successor in successors:
                if successor not in explored:
                    frontier.push(successor)
        return False

    # A static fuction that return a numpy array of unsigned integer based on a given list if possible.
    # If impossible exit code with error message.
    def get_valid_array(arr: List) -> np.ndarray:
        try:
            arr = np.array(arr, dtype=np.int32)
        except:
            errors_handler("Data-Error", 0)
        for item in arr:
            if(item < 0):
                errors_handler("Data-Error", 0)
        return arr

class Queue:
    # A container with a first-in-first-out (FIFO) queuing policy.
    def __init__(self):
        self.list = []
    
    # Enqueue the 'item' into the queue
    def push(self,item: any):
        self.list.insert(0,item)

    # Dequeue the earliest enqueued item still in the queue. This
    # operation removes the item from the queue.
    def pop(self) -> any:
        return self.list.pop()

    # Returns true if the queue is empty
    def isEmpty(self) -> bool:
        return len(self.list) == 0

# exit the code with a given message colored in red.
def exit_message(msg: str):
    print(colored("\n"+ msg +"\n", 'red', attrs=['bold']))
    sys.exit()

def errors_handler(errorType: str, errorCode: int):
    if(errorType == "Data-Error"):
        if(errorCode == 0):
            exit_message("Data-Error: invalid file content.\nError-code: 0 \nThe contents should contains only sequentially arrays of unsigned integers.")
        elif(errorCode == 1):
            exit_message("Data-Error: empty file. \nError-code: 1")
        elif(errorCode == 2):
            exit_message("Data-Error: invalid json format. \nError-code: 2\nOnly Json of a single array or array of arrays are valid for this process.")
    elif(errorType == "File-Error"):
        if(errorCode == 0):
            exit_message("File-Error: invalid file extension in input path.\nError-code: 0\nvalid extensions are only of types: CSV, TSV, JSON.")
        elif(errorCode == 1):
            exit_message("File-Error: File could not open correctly.\nError-code: 1")
    elif(errorType == "Input-Error"):
        if(errorCode == 0):
            exit_message("Input-Error: missing arguments.\nError-code: 0 \nPlease give a file path as argument using '--input_path'.")
    else:
        exit_message("Handler-Error: Incorrect use of errors_handler.\nError-code: -1")

def get_csv_or_tsv_data(fileReader) -> List[np.ndarray]:
    data = []
    for row in fileReader:   
        if(any(field.strip() for field in row)):#ignore empty rows
            max = len(row) -1
            index  = None
            for index in range(max, 0, -1):
                if(row[index] != ''):
                    break
            row = row[:index+1]
            row = WearyArrayTraveler.get_valid_array(row)
            data.append(row)
    if(not data):#empty file case
       errors_handler("Data-Error", 1)
    return data

def get_json_data(fileReader: List) -> List[np.ndarray]:
    data = []
    try:
        if(not fileReader):#empty file case
            errors_handler("Data-Error", 1)
        elif(isinstance(fileReader[0], int)):#single row (array) for json case - cannot loop the fileReader because then we iterate the items instead of the rows
            row = WearyArrayTraveler.get_valid_array(fileReader)
            data.append(row)
        else:
            for row in fileReader:
                if(row):#ignore empty rows
                    row = WearyArrayTraveler.get_valid_array(row)
                    data.append(row)
        return data
    except:
        errors_handler("Data-Error", 2)

def get_file_data(path: str) -> List[np.ndarray]:
    pathLowerCase = path.lower()
    try:
        file = open(path, 'r')
    except:
        errors_handler("File-Error", 1)
    if(pathLowerCase.endswith(".csv")):
        data = get_csv_or_tsv_data(csv.reader(file))
    elif(pathLowerCase.endswith(".tsv")):
        data = get_csv_or_tsv_data(csv.reader(file, delimiter="\t"))
    elif(pathLowerCase.endswith(".json")):
        data = get_json_data(json.load(file))
    else:
        errors_handler("File-Error", 0)
    file.close()
    return data

def get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="", help="Path to the input (may came in 3 formats: CSV, TSV, JSON)")
    return parser

def main(args: any) -> None:
    if(args.input_path == ""):
        errors_handler("Input-Error", 0)
    data = get_file_data(args.input_path)
    wearyArrayTraveler = WearyArrayTraveler()
    table = PrettyTable(['Arrays', 'Traverseable'])
    counter = 1 # counter to points the current array number
    for arr in data:
        travelResult = wearyArrayTraveler.is_array_traverseable(arr)
        table.add_row(['Array number '+ str(counter), travelResult])
        counter += 1
    table.align = "l" # align table left
    print(table)

if __name__ == '__main__':
    init() # for coloring error messages 
    parser = get_args_parser()
    try:
        args = parser.parse_args()
    except:
        errors_handler("Input-Error", 0)
    main(args)
