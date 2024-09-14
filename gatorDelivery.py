import sys
import re
class Node:
    def __init__(self, order_id, current_system_time, orderValue, deliveryTime):
        # Node data
        self.order_id = order_id
        self.current_system_time = current_system_time
        self.orderValue = orderValue 
        self.deliveryTime = deliveryTime
        self.ETA = None
        
        # key
        self.priority = 0.3*(self.orderValue/50)-(0.7*current_system_time)

        
        # Node structure
        self.left = None
        self.right = None
        self.height = 1



    # method
    def get_path(self, orderId): # get the path from node to root
        if self.order_id == orderId:
            return [self]
        if self.left != None:
            path = self.left.get_path(orderId)
            if path :
                path.append(self)
                return path
        if self.right != None:
            path = self.right.get_path(orderId)
            if path :
                path.append(self)
                return path


    def get_closest_big(self, orderId): # get the closet node which priority is greater than the current node
        path = self.get_path(orderId)
        if path[0].right :
            right = path[0].right
            while right.left:
                right = right.left
            return right
        for path_node in path:
            if path_node.priority > path[0].priority:
                # print(str(path_node.priority)+ " "+str (path[0].priority))
                return path_node
            




class AVLTree:
    # data
    def __init__(self):
        self.root = None
        self.returnTime = 0
    
    # def get_closest_big(self, orderId):
    #     array = []
    #     self.getAllOrderInOrder(self.root, array)
    #     i = 0
    #     while i < len(array):
    #         if array[i].order_id == orderId:
    #             break
    #         i+=1
    #     if i == 0:
    #         return 
    #     else:
    #         return array[i-1]

        

    def print(self, orderId):
        node_list = self.root.get_path(orderId)
        print("["+str(node_list[0].order_id) +", "+str(node_list[0].current_system_time)+", "+str(node_list[0].orderValue)+", "+str(node_list[0].deliveryTime)+", "+str(node_list[0].ETA)+" ]")

    def print1(self, time1, time2): # Prints all the orders that will be delivered within the given times (including both
# times) and are undelivered.
        array = []
        self.getAllOrderInOrder(self.root, array)
        result = []
        for i in range(len(array)):
            if array[i].ETA >= time1 and array[i].ETA <= time2:
                result.append(array[i])
        if len(result) == 0:
            print("There are no orders in that time period")
        else:

            s = "["
            j = 0
            for ele in result:
                s += str(ele.order_id)
                if j != len(result)-1:
                    s += ", "
                j+=1
            s+="]"
            print(s)

    def getRankOfOrder(self, orderId):  # Takes the order_id and returns how many orders will be delivered before it.
        # priority = self.root.get_path(orderId)[0].priority
        # count = [0]
        # self.getRank(self.root, priority,count)
        # return count[0]
        OrderArray = []
        self.getAllOrderInOrder(self.root, OrderArray)
        count = 0
        for i in range(len(OrderArray)):
            if OrderArray[i].order_id != orderId:
                count += 1
            else:
                break
        if count < len(OrderArray):
            print("Order "+ str(orderId)+" will be delivered after "+str(count)+" orders.")
        return count
    
    # def getRank(self, root, priority, count):
    #     if not root:
    #         return
    #     self.getRank(root.right, priority, count)
    #     if root.priority <= priority:
    #         return
    #     else:
    #         count[0]+=1
    #     self.getRank(root.left, priority, count)


    def getAllOrderInOrder(self, root, array): # return an array that list all the orders in order
        if not root:
            return
        self.getAllOrderInOrder(root.right,array)
        array.append(root)
        self.getAllOrderInOrder(root.left, array)
        return array


            

    def createOrder(self, order_id, current_system_time, orderValue, deliveryTime):
        deliveredArray = self.alreadyDelievered(current_system_time)

        node = Node(order_id, current_system_time, orderValue, deliveryTime)
        # if the first order have already been delivered out, then turn its priority to 100
        firstArray = []
        self.getAllOrderInOrder(self.root, firstArray) 
        if len(firstArray) != 0:
            firstOrder = firstArray[0]
            if (node.priority > firstOrder.priority) and ((firstOrder.ETA - firstOrder.deliveryTime) <= current_system_time):
                firstOrder.priority = 100

        
        self.root = self.insert(self.root, node)
        # calculate ETA
        bigger_node = self.root.get_closest_big(order_id) 
        if not bigger_node:
            if self.returnTime < current_system_time:
                node.ETA = current_system_time+deliveryTime
            else:
                node.ETA = self.returnTime + deliveryTime
        else:
            node.ETA = bigger_node.ETA+bigger_node.deliveryTime+node.deliveryTime
        print("Order "+ str(node.order_id)+ " has been created - ETA: "+str(node.ETA))
        
        # check if there is any order update
        i = 0
        array = []
        self.getAllOrderInOrder(self.root, array)
        while i < len(array):
            if array[i].order_id == order_id:
                break
            i+=1
        i+=1
        updateOrder = []
        while i < len(array):
            array[i].ETA = array[i-1].ETA + array[i-1].deliveryTime + array[i].deliveryTime
            updateOrder.append(array[i])
            i+=1
        if len(updateOrder) != 0:
            s = "Updated ETAs: ["
            j = 0
            while j < len(updateOrder):
                s += str(updateOrder[j].order_id)+": "+str(updateOrder[j].ETA)
                if j != len(updateOrder)-1:
                    s += ", "
                j += 1
            s += "]"
            print(s)
                

            


        self.printAlreadyDelievered(deliveredArray)

    def insert(self, root, node): # Insert a new node in the current AVL tree.
        if not root: # if root not exist
            return node
        elif node.priority < root.priority:
            root.left = self.insert(root.left, node)
        else:
            root.right = self.insert(root.right, node)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        # Left Heavy
        if balance > 1 and node.priority < root.left.priority:
            return self.rightRotate(root)

        # Right Heavy
        if balance < -1 and node.priority > root.right.priority:
            return self.leftRotate(root)

        # Left Right Case
        if balance > 1 and node.priority > root.left.priority:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Right Left Case
        if balance < -1 and node.priority < root.right.priority:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, x): # Perform left rotate in a AVL tree.
        y = x.right
        z = y.left

        y.left = x
        x.right = z

        x.height = 1 + max(self.getHeight(x.left),
                           self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def rightRotate(self, x): # Perform right rotate in a AVL tree.
        y = x.left
        z = y.right

        y.right = x
        x.left = z

        x.height = 1 + max(self.getHeight(x.left),
                           self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def getHeight(self, root): # Return the height of current node
        if not root:
            return 0

        return root.height

    def getBalance(self, root): # Return the balance of current
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root): # trace the structure of the AVL tree
        if not root:
            return
        self.preOrder(root.left)
        # print("{0} ".format(root.order_id), end="")
        print(root.order_id)
        self.preOrder(root.right)

    def updateTime(self, order_id, current_system_time, newDeliveryTime):
        deliveredArray = self.alreadyDelievered(current_system_time)
        array = []       
        self.getAllOrderInOrder(self.root, array)
        i = 0
        while i < len(array):
            if array[i].order_id == order_id:
                break
            i+=1

        if i == len(array):
            print("Cannot update. Order " + str(order_id) + " has already been delivered.")
        
        else:
            if (array[i].ETA - array[i].deliveryTime) <= current_system_time: # (array[i].ETA - array[i].deliveryTime) 是從配貨中心運送出去包裹的時間點
                print("Cannot update. Order "+str(order_id)+" is out for delivery.")
            else:
                dif = newDeliveryTime - array[i].deliveryTime
                array[i].deliveryTime = newDeliveryTime
                array[i].ETA = array[i].ETA + dif

                j=i+1
                while j < len(array):
                    array[j].ETA = array[j].ETA + 2*dif
                    j+=1
                
                s = "Updated ETAs: ["
                while i < len(array):
                    s += str(array[i].order_id)+": "+str(array[i].ETA)
                    if i != len(array)-1:
                        s += ", "
                    i += 1
                s += "]"
                print(s)
        self.printAlreadyDelievered(deliveredArray)

    def cancelOrder(self, order_id, current_system_time):
        deliveredArray = self.alreadyDelievered(current_system_time)
        array = []
        self.getAllOrderInOrder(self.root, array)
        i = 0


        while i < len(array):
            if array[i].order_id == order_id:
                break
            i+=1

        if i == len(array): # couldn't find the package
            print("Cannot cancel. Order "+str(order_id)+" has already been delivered.")
        else: # after find the package
            # 如果此刻的時間已經超過原預計送出的時間(包裹已在路上) if package is on the way
            if (array[i].ETA - array[i].deliveryTime) < current_system_time: # (array[i].ETA - array[i].deliveryTime) is when the package is picked up at the delivery center
                print("Cannot cancel. Order "+str(order_id)+" is out for delivery.")
            else:
                updatedOrder = []
                if i == len(array)-1: # if the cancelled order was the last order, no other need order need to be updated
                    pass
                elif i == 0 : # if the cancelled order was originally the next order and there are at least one order after canceling
                    k = i+1
                    array[k].ETA = self.returnTime+array[k].deliveryTime # decided by the returning time of the delivery agent
                    updatedOrder.append(array[k])
                    k+=1
                    while k < len(array):
                        array[k].ETA = array[k-1].ETA + array[k-1].deliveryTime + array[k].deliveryTime
                        updatedOrder.append(array[k])
                        k+=1
                else: # if the cancelled order has order before and after it
                    k = i+1
                    array[k].ETA =  array[k-2].ETA + array[k-2].deliveryTime + array[k].deliveryTime # decided by the order before the cancelled order
                    updatedOrder.append(array[k])
                    k+=1
                    while k < len(array):
                        array[k].ETA = array[k-1].ETA + array[k-1].deliveryTime + array[k].deliveryTime
                        updatedOrder.append(array[k])
                        k+=1

                print("Order "+str(order_id)+" has been canceled")
                if len(updatedOrder) != 0:
                    s = "Updated ETAs: ["
                    j = 0
                    while j < len(updatedOrder):
                        s += str(updatedOrder[j].order_id)+": "+str(updatedOrder[j].ETA)
                        if j != len(updatedOrder)-1:
                            s += ", "
                        j += 1
                    s += "]"
                    print(s)
                self.root = self.delete(self.root, array[i].priority)
            # if i != 0: # 如果要cancel的不是下一個包裹
            #     deleteOrder = array[i]
            #     beforeDeleteOrder = array[i-1]
            #     returnTime = beforeDeleteOrder.ETA + beforeDeleteOrder.deliveryTime
            # if i==0: # 下一個包裹剛好是要cancel的包裹，分成來得及與來不及cancel兩種狀況
            #     if returnTime < current_system_time: # 來不及刪除
            #         print("Order "+str(order_id)+" has already been delivered if the order is out for delivery or is already delivered")
            #     else: # 如果還來的及刪除，下一個修正後，後面跟著前面修正
            #         j = i + 1
            #         if j < len(array): 
            #             array[j].ETA = returnTime + array[j].deliveryTime
            #             j += 1

            #         while j < len(array):
            #             array[j].ETA = array[j-1].ETA + array[j-1].ETA + array[j].deliveryTime
            #             j+=1
                
            # else: # 來得及取消
            #     j = i + 1
            #     if j < len(array): 
            #         array[j].ETA = returnTime + array[j].deliveryTime
            #         j += 1

            #     while j < len(array):
            #         array[j].ETA = array[j-1].ETA + array[j-1].ETA + array[j].deliveryTime
            #         j+=1

            


        self.printAlreadyDelievered(deliveredArray)


    def delete(self, root, priority): # delete a node from the AVL tree
 
        # Step 1 - Perform standard BST delete
        if not root:
            return root
 
        elif priority < root.priority:
            root.left = self.delete(root.left, priority)
 
        elif priority > root.priority:
            root.right = self.delete(root.right, priority)
 
        else:
            if not root.left:
                return root.right
 
            elif not root.right:
                return root.left
 
            temp = self.getMinValueNode(root.right)
            root.priority = temp.priority
            root.order_id = temp.order_id
            root.current_system_time = temp.current_system_time
            root.orderValue = temp.orderValue 
            root.deliveryTime = temp.deliveryTime
            root.ETA = temp.ETA
            root.right = self.delete(root.right,
                                      temp.priority)
 
 
        # Update the height of the 
        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))
 
        # Get the balance
        balance = self.getBalance(root)
 
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
    
    def getMinValueNode(self, root): # Get the minimum node of a subtree
        if root is None or root.left is None:
            return root
 
        return self.getMinValueNode(root.left)
    
    def alreadyDelievered(self, current_time): # get all orders that should have been delivered at the current time
        array = []
        self.getAllOrderInOrder(self.root, array)
        result = []
        for i in range(len(array)):
            if array[i].ETA <= current_time:
                result.append(array[i])
                self.returnTime = array[i].ETA +  array[i].deliveryTime
                self.root = self.delete(self.root, array[i].priority)
            else:
                break
        return result
        

    def printAlreadyDelievered(self, array): # print all orders that have been delivered at the current time
        for ele in array:
            print("Order "+str(ele.order_id)+" has been delivered at time "+ str(ele.ETA))

    def Quit(self):
        array = []
        self.getAllOrderInOrder(self.root, array)
        for i in range(len(array)):
            print("Order "+str(array[i].order_id)+" has been delivered at time "+ str(array[i].ETA))




if __name__ == "__main__":
    myTree = AVLTree()
    filename = sys.argv[1]
    with open(filename, 'r') as file:
    # Read the entire file content into a string
        content = file.readlines()
        for i in range(len(content)):
            content[i] = content[i].split("\n")[0]

        # print(content)
    
    sys.stdout = open(filename.split('.')[0]+'_output_file.txt', 'w')
    pattern = r'(\w+)\((.*)\)'
    for i in range(len(content)):
        matches = re.match(pattern, content[i])
        function_name = matches.group(1)
        arguments = matches.group(2).split(',')
        arguments = [arg.strip() for arg in arguments]
        # print("Function name:", function_name)
        # print("Arguments:", arguments)
        if function_name == "createOrder":
            myTree.createOrder(int(arguments[0]),int(arguments[1]),int(arguments[2]),int(arguments[3]))
        elif ((function_name == "print") and (len(arguments) == 2)):
            myTree.print1(int(arguments[0]),int(arguments[1]))
        elif ((function_name == "print") and (len(arguments) == 1)):
            myTree.print(int(arguments[0]))
        elif function_name == "getRankOfOrder":
            myTree.getRankOfOrder(int(arguments[0]))
        elif function_name == "cancelOrder":
            myTree.cancelOrder(int(arguments[0]),int(arguments[1]))
        elif function_name == "updateTime":
            myTree.updateTime(int(arguments[0]),int(arguments[1]),int(arguments[2]))
        elif function_name == "Quit":
            myTree.Quit()
        




    # myTree.createOrder(1001, 1, 200, 3)
    # myTree.createOrder(1002, 3, 250, 6)
    # myTree.createOrder(1003, 8, 100, 3)
    # myTree.createOrder(1004, 13, 100, 5)
    # myTree.print(2,15)
    # myTree.updateTime(1003,15,1)
    # myTree.createOrder(1005, 30, 300, 3)
    # myTree.Quit()
    
    # TestCase 1:
    # myTree.createOrder(1001, 1, 100, 4)
    # myTree.createOrder(1002, 2, 150, 7)
    # myTree.createOrder(1003, 8, 50, 2)
    # myTree.print(2,15)
    # myTree.createOrder(1004, 9, 300, 12)
    # myTree.getRankOfOrder(1004)
    # myTree.print(45, 55)
    # myTree.createOrder(1005, 15, 400, 8)
    # myTree.createOrder(1006, 17, 100, 3)
    # myTree.cancelOrder(1005, 18)
    # myTree.getRankOfOrder(1004)
    # myTree.createOrder(1007, 19, 600, 7)
    # myTree.createOrder(1008, 25, 200, 8)
    # myTree.updateTime(1007, 27, 12)
    # myTree.getRankOfOrder(1006)
    # myTree.print(55,85)
    # myTree.createOrder(1009, 36, 500, 15)
    # myTree.createOrder(1010, 40, 250, 10)
    # myTree.Quit()

    # TestCase 2:
    # myTree.createOrder(3001, 1, 200, 7)
    # myTree.createOrder(3002, 3, 250, 6)
    # myTree.createOrder(3003, 8, 1000, 3)
    # myTree.createOrder(3004, 13, 100, 5)
    # myTree.createOrder(3005, 15, 300, 4)
    # myTree.createOrder(3006, 17, 800, 2)
    # myTree.print(2,20)
    # myTree.updateTime(3004, 20, 2)
    # myTree.print(5,25)
    # myTree.cancelOrder(3005, 25)
    # myTree.print(10,30)
    # myTree.createOrder(3007, 30, 200, 3)
    # myTree.getRankOfOrder(3005)
    # myTree.createOrder(3008, 33, 250, 6)
    # myTree.createOrder(3009, 38, 100, 3)
    # myTree.createOrder(3010, 40, 4000, 5)
    # myTree.getRankOfOrder(3008)
    # myTree.createOrder(3011, 45, 300, 4)
    # myTree.createOrder(3012, 47, 150, 2)
    # myTree.print(35,50)
    # myTree.getRankOfOrder(3006)
    # myTree.Quit()

    
    # testCase 3:
    # myTree.createOrder(4001, 1,200,3)
    # myTree.createOrder(4002, 3, 250, 6)
    # myTree.createOrder(4003, 8, 100, 3)
    # myTree.createOrder(4004, 13, 100, 5)
    # myTree.print(2, 15)
    # myTree.getRankOfOrder(4003)
    # myTree.updateTime(4003, 15, 2)
    # myTree.createOrder(4005, 17, 150, 4)
    # myTree.cancelOrder(4002, 20)
    # myTree.createOrder(4006, 22, 300, 3)
    # myTree.print(10, 25)
    # myTree.createOrder(4007, 25, 200, 2)
    # myTree.createOrder(4008, 28, 350, 5)
    # myTree.print(20, 30)
    # myTree.getRankOfOrder(4006)
    # myTree.createOrder(4009, 32, 250, 3)
    # myTree.cancelOrder(4004, 34)
    # myTree.updateTime(4005, 37, 5)
    # myTree.createOrder(4010, 40, 400, 6)
    # myTree.print(35, 45)
    # myTree.getRankOfOrder(4007)
    # myTree.createOrder(4011, 40, 200, 4)
    # myTree.createOrder(4012, 42, 300, 3)
    # myTree.print(50, 55)
    # myTree.updateTime(4010, 55, 7)
    # myTree.cancelOrder(4009, 56)
    # myTree.print(60, 90)
    # myTree.Quit()


    # print("Preorder traversal of constructed tree is :")
    # path_list = myTree.root.get_path(1001)
    # for x in range(len(path_list)):
    #     print (path_list[x].order_id)
    #     print (path_list[x].priority)

    # print(myTree.root.get_closest_big(1004).order_id)
    # print(myTree.getRankOfOrder(1004))
    # myTree.print(1001)
    # myTree.print(1002)
    # myTree.print(1003)
    # myTree.print(1004)
    # myTree.updateTime(1002, 4, 5)
    # myTree.cancelOrder(1001,9)
    # myTree.preOrder(myTree.root)

