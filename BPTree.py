import copy

class Node:     # Structure for a node
    def __init__(self, isLeaf=False, key=[], parent=None, next=None, prev=None, child=[]):
        self.isLeaf = isLeaf
        self.key = key
        self.parent = parent
        self.next = next
        self.prev = prev
        self.child = child

    def __del__(self):
        return

# Global variable
order = 1       # order
root = None     # root

def options():              # 使用者操作介面
    option = ["Initialize","Attach","Bulkload","Lookup","Insert","Delete","Display","Quit"]

    for i in range(4):
        print('{}){:<16s}'.format(i+1, option[i]), sep='', end='')
    print()
    for i in range(4, 8):
        print('{}){:<16s}'.format(i+1, option[i]), sep='', end='')
    print()
    
    choice = int( input('> Select an operation: ') )
    return choice

def init():                 # 1: 獲取新的 tree，初始化 root node
    global order, root
    order = int( input('Initializing... order = ') )
    if order < 1:           # Invalid order
        print("Invalid order number!! Initializing failed...")
        root = None
        return

    root = Node(True, [], None, None, None, [])
    return

def find(node, element):    # 尋找向下尋找的分支(child)
    if element < node.key[0]:       # Left-most child
        return 0
    
    size = len(node.key)            # Right-most child
    if element >= node.key[size-1]:
        return size

    for i in range(size-1):         # other child
        if element>=node.key[i] and element < node.key[i+1]:
            return i+1

def toLeaf(kkey):           # 尋找 kkey 所在的 Leaf Node
    global root
    tmp = root
    while not tmp.isLeaf:
        idx = find(tmp, kkey)
        tmp = tmp.child[idx]
    return tmp

def lookup(kkey=-1):        # 4: 尋找某 key 是否存在 Tree 中
    global root
    if not root:        # There is no Tree
        print("There is no Tree.")
        return

    if kkey == -1:      # Read the key
        kkey = int( input('Searching... key = ') )

    tmp = toLeaf(kkey)

    if kkey in tmp.key:
        return True
    else:
        return False

def printRecur(node):       # Inorder 遞迴遍歷 Tree
    size = len(node.key)
    if not node.isLeaf:     # Non-leaf, keep recursive
        for i in range(size):
            printRecur(node.child[i])
            print('; {} ;'.format(node.key[i]), end=' ')
        printRecur(node.child[size])
    else:                   # Leaf, print keys only
        for i in range(size):
            print('{}'.format(node.key[i]), end=' ')

    return

def countLen(node, idx):    # 計算print格式化長度
    if node.isLeaf:         # Leaf node，回傳key數量
        return len(node.key)
    else:
        if idx != -1:       # 第一次遞迴，算單個key所需的長度
            return countLen(node.child[idx], -1)
        else:
            sum = 0         # 算出整個node所需的長度
            for item in node.child:
                sum += countLen(item, -1)
            return sum

def printBlank(node, idx):  # 專門印出空格
    if node.isLeaf:            # Leaf node不需要空格
        return

    if idx != len(node.key):   # 最後一個key補齊長度，其他減少一格
        length = countLen(node, idx) - 1
    else:
        length = countLen(node, idx)

    for i in range(length):
        print('     ', end='')
    return

def printLevel():           # 按 Level 印出 Tree
    global root

    lastL = 0           # 記錄last level
    que = [[root, 0]]   # queue
    while que:
        [item, level] = que.pop(0)
        if lastL+1 == level:              # level變了，印換行
            print()
        
        # 印出最前面的空格，整行的最前面且non-leaf再加上3空格
        printBlank(item, 0)
        if (lastL+1 == level or level == 0) and not item.isLeaf:
            print('   ',end='')
        
        for i in range( len(item.key) ):  # 印出key及後面的空格
            print('{:^5d}'.format(item.key[i]), end='')
            printBlank(item, i+1)

        if not item.isLeaf:               # 將non-Leaf node的child放入queue中
            for children in item.child:
                que.append([children, level+1])
        lastL = level                     # 記下node的level，用於檢查是否要印換行
    print()

    return

def display():              # 7: Inorder 印出 Tree
    global root
    if not root:     # There is no Tree
        print('There is no Tree to display.')
        return

    print('Display inorder:')
    printRecur(root) # Start recursive
    print()
    print()

    print('Display level-by-level:')
    printLevel()     # Print level-by-level

    return

def spilt(node):            # key 數量過多，挑出一個 key 往上推
    global root, order
    middle = node.key[order]

    # Leaf or Non-leaf
    if node.isLeaf:         # Leaf
        nnew = Node(isLeaf=True, key=copy.deepcopy(node.key[order:]), prev=node)
        node.next = nnew 
        del node.key[order:]
    else:                   # Non-leaf
        nnew = Node(isLeaf=False, key=copy.deepcopy(node.key[order+1:]), child=node.child[order+1:])
        for i in range( len(nnew.child) ):
            nnew.child[i].parent = nnew
        del node.key[order:]
        del node.child[order+1:]

    # root or not
    if node == root:        # root
        root = Node(isLeaf=False, key=copy.deepcopy([middle]), child=[node, nnew])
        nnew.parent = root
        node.parent = root
    else:                   # not root
        par = node.parent
        nnew.parent = par
        idx = find(par, middle)
        par.key.insert(idx, middle)
        par.child.insert(idx+1, nnew)

        if len(par.key) > order*2:  # 上層node的key太多，遞迴處理
                spilt(par)

    return

def insert(kkey=-1):        # 5: 加入一個 key
    global root, order
    if not root:    # There is no Tree
        print("Invalid insert, B+ Tree hasn't be initialized yet.")
        return
    
    if kkey == -1:  # Read the key
        kkey = int( input('Inserting... key = ') )

    tmp = toLeaf(kkey)
    tmp.key.append(kkey)        # Add key into key
    tmp.key.sort()

    if len(tmp.key) > order*2:  # Invalid tree, do pushing up a key
        spilt(tmp)

    return

def attach():               # 2: 建立 Tree
    global order, root
    order = int( input('Attaching... order = ') )
    if order < 1:
        print("Invalid order number!! Initializing failed...")
        return

    # Data processing
    indata = input('Nodes in inorder-like traversal = ')
    indata = indata.split(";")
    leaf = []
    nonL = []
    for i in range( len(indata) ):
        indata[i] = indata[i].split()
        indata[i] = [int(x) for x in indata[i]]
        if i%2 == 0:    # Leaf Node
            leaf.append(indata[i])
        else:           # Non-leaf Node
            nonL.extend(indata[i])

    # Link all Leaf Node and 填入 queue
    que = []
    leafStart = Node(True, copy.deepcopy(leaf[0]), None, None, None, [])
    prev = leafStart
    que.append(leafStart)
    for i in range(1,len(leaf)):
        newL = Node(True, copy.deepcopy(leaf[i]), None, None, prev, [])
        que.append(newL)
        prev.next = newL
        prev = newL

    # Start building the Tree
    while len(que) > 1:
        tnonL = []      # tmp nonL
        while nonL:     # start to clear nonL
            idx = min(2*order, len(nonL))   # order個 或 len()個 key
            curNode = Node(False, copy.deepcopy(nonL[0:idx]), None, None, None, que[0:idx+1])
            for i in range(idx+1):          # fill the parent
                que[i].parent = curNode
            del nonL[0:idx]                 # 處理過的nonL
            del que[0:idx+1]
            que.append(curNode)             # push into queue
            if nonL:
                tnonL.append( nonL.pop(0) ) # higher nonL
        nonL = tnonL
    root = que[0]       # root Node is the highest

    return

def bulkload():             # 3: 大量 insert keys
    global root
    if not root:    # There is no Tree
        print("Invalid bulkload, B+ Tree hasn't be initialized yet.")
        return

    # Read user input
    indata = input('Bulkloading... key sequence = ')
    num = indata.split()
    num = [int(i) for i in num]

    # Sort the input and insert key one-by-one
    num.sort()
    for number in num:
        insert(number)

    return

def merge(nodeA, nodeB):    # nodeB 合併到 nodeA
    global root             # nodeA < nodeB

    # 找到nodeB位於parent.child的index，要刪掉
    for i in range( len(nodeA.parent.child) ):
        if nodeA.parent.child[i] == nodeB:
            idx = i
            break

    # 分成 leaf 與 non-leaf 處理
    if nodeA.isLeaf:    # 2 node 都是 leaf node
        nodeA.key.extend(nodeB.key)

        nodeA.next = nodeB.next
        if nodeB.next:
            nodeB.next.prev = nodeA

        del nodeA.parent.key[idx-1]
        del nodeA.parent.child[idx]
    else:               # 2 node 都是 non-leaf
        # 更改nodeB的child的parent
        for item in nodeB.child:
            item.parent = nodeA

        nodeA.child.extend(nodeB.child)
        nodeA.key.append( nodeA.parent.key.pop(idx-1) )
        nodeA.key.extend(nodeB.key)

        del nodeA.parent.child[idx]
    
    # root為空，改root
    if nodeA.parent == root and len(root.key) == 0:
        root = nodeA
        root.parent = None
        return

    # 檢查是否繼續merge
    if len(nodeA.parent.key) < order:
        adjust(nodeA.parent)

    return

def borrow(nodeA, nodeB, asc):# nodeA 借1個key給 nodeB
    # asc==True -> nodeA < nodeB
    # 找到nodeB位於parent.child的index
    for i in range( len(nodeA.parent.child) ):
        if nodeA.parent.child[i] == nodeB:
            idx = i
            break

    if nodeA.isLeaf:        # 2 node 皆為 leaf node
        if asc:     # nodeA < nodeB
            nodeB.key.insert(0, nodeA.key.pop())
            nodeA.parent.key[idx-1] = nodeB.key[0]
        else:       # nodeA > nodeB
            nodeB.key.append( nodeA.key.pop(0) )
            nodeA.parent.key[idx] = nodeA.key[0]
    else:                   # 2 node 都為 non-leaf
        if asc:     # nodeA < nodeB
            nodeB.key.insert(0, nodeA.parent.key[idx-1])
            nodeA.parent.key[idx-1] = nodeA.key.pop()
            nodeB.child.insert(0, nodeA.child.pop())
            nodeB.child[0].parent = nodeB
        else:       # nodeA > nodeB
            nodeB.key.append(nodeA.parent.key[idx])
            nodeA.parent.key[idx] = nodeA.key.pop(0)
            nodeB.child.append( nodeA.child.pop(0) )
            nodeB.child[len(nodeB.child)-1].parent = nodeB
    return

def adjust(node):           # delete後的redistribution
    global root, order
    if node == root:        # root不需要調整沒關係
        return

    if node.isLeaf:         # Leaf node
        if node.prev and node.prev.parent == node.parent and len(node.prev.key) > order:
            borrow(node.prev, node, True)
        elif node.next and node.next.parent == node.parent and len(node.next.key) > order:
            borrow(node.next, node, False)
        elif node.prev and node.prev.parent == node.parent:
            merge(node.prev, node)
        elif node.next and node.next.parent == node.parent:
            merge(node, node.next)
    else:                   # Non-leaf node
        for i in range( len(node.parent.child) ):
            if node.parent.child[i] == node:
                idx = i
                break
        if idx == 0:        # 最左邊的node
            if len(node.parent.child[1].key) > order:
                borrow(node.parent.child[1], node, False)
            else:
                merge(node, node.parent.child[1])
        elif idx == len(node.parent.child) - 1:  # 中間的node
            if len(node.parent.child[idx-1].key) > order:
                borrow(node.parent.child[idx-1], node, True)
            else:
                merge(node.parent.child[idx-1], node)
        else:               # 最右邊的node
            if len(node.parent.child[idx-1].key) > order:
                borrow(node.parent.child[idx-1], node, True)
            elif len(node.parent.child[idx+1].key) > order:
                borrow(node.parent.child[idx+1], node, False)
            else:
                merge(node.parent.child[idx-1], node)
    return

def dele(kkey = -1):        # 6: 刪除一個指定 key
    global root
    if not root:    # There is no Tree
        print("There is no Tree.")
        return

    if kkey == -1:  # Read the key
        kkey = int( input('Deleting... key = ') )

    tmp = toLeaf(kkey)

    if kkey not in tmp.key:
        print("{} isn't in Tree.".format(kkey))
    else:
        tmp.key.remove(kkey)

    if len(tmp.key) < order:# Check if the amount of key is legal
        adjust(tmp)
            
    return

def main():                 # Main Function
    while 1:    # Keep receiving operation
        choice = options()

        if choice == 1:
            init()
        elif choice == 2:
            attach()
        elif choice == 3:
            bulkload()
        elif choice == 4:
            print( lookup() )
        elif choice == 5:
            insert()
        elif choice == 6:
            dele()
        elif choice == 7:
            display()
        elif choice == 8:
            print('Quit.')
            break
        else:
            print('Invalid option, please select again.')
    
        print()

    return

main()