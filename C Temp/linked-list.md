# C Programming - Linked List (লিংকড লিস্ট)

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Linked List কী এবং কেন?](#linked-list-কী-এবং-কেন)
3. [Array vs Linked List](#array-vs-linked-list)
4. [Node Structure](#node-structure)
5. [Types of Linked Lists](#types-of-linked-lists)
6. [Singly Linked List Operations](#singly-linked-list-operations)
7. [Complete Implementation](#complete-implementation)
8. [Memory Management](#memory-management)
9. [Common Problems](#common-problems)

---

## পরিচিতি

Linked List হলো একটা dynamic data structure যেখানে elements (nodes) pointer দিয়ে connected থাকে।

### Prerequisites:

আগে **[Pointers](pointers.md)** ভালো করে বুঝে নিন! Linked List সম্পূর্ণভাবে pointer এর উপর নির্ভরশীল।

---

## Linked List কী এবং কেন?

### Linked List কী?

**সহজ ভাষায়:** Linked List হলো nodes এর একটা chain যেখানে প্রতিটা node পরের node এর address রাখে।

```
Node 1 → Node 2 → Node 3 → Node 4 → NULL
```

### Real-World উদাহরণ:

```
Train এর Bogies:

[Engine] → [Bogie 1] → [Bogie 2] → [Bogie 3] → NULL

প্রতিটা bogie:
- নিজের data আছে (যাত্রী, মালপত্র)
- পরের bogie এর সাথে connected (coupling)
- শেষ bogie এর পরে কিছু নেই (NULL)

Features:
- নতুন bogie যোগ করা সহজ (যেকোনো জায়গায়)
- Bogie সরানো সহজ
- যতগুলো চাই ততগুলো যোগ করা যায়
```

### কেন Linked List?

**Array এর সমস্যা:**

```c
int arr[5];  // শুধু 5টা element

// সমস্যা ১: Fixed size
// আরো element চাইলে? নতুন array বানাতে হবে!

// সমস্যা ২: Insertion/Deletion কঠিন
// Middle এ insert করতে হলে সব shift করতে হবে
```

**Linked List এর সুবিধা:**

```c
// ✅ Dynamic size - যতগুলো চাই ততগুলো
// ✅ Easy insertion - যেকোনো জায়গায়
// ✅ Easy deletion - যেকোনো জায়গা থেকে
// ✅ Memory efficient - যতটুকু দরকার ততটুকু
```

---

## Array vs Linked List

### Comparison:

| Feature | Array | Linked List |
|---------|-------|-------------|
| **Size** | Fixed | Dynamic |
| **Memory** | Continuous | Scattered |
| **Access** | O(1) - Direct | O(n) - Sequential |
| **Insertion** | O(n) - Shift needed | O(1) - Just pointer change |
| **Deletion** | O(n) - Shift needed | O(1) - Just pointer change |
| **Memory Waste** | Yes (unused space) | No (exact size) |

### Memory Layout:

```
Array:
Memory: [10][20][30][40][50]
        ↑   ↑   ↑   ↑   ↑
Address: 1000 1004 1008 1012 1016
        (Continuous - পাশাপাশি)

Linked List:
Memory: [10|→] ... [20|→] ... [30|→] ... [40|→] ... [50|NULL]
        ↑           ↑           ↑           ↑           ↑
Address: 1000       2500        1200        3000        1500
        (Scattered - যেখানে সেখানে)
```

---

## Node Structure

### Node কী?

Node হলো Linked List এর building block। প্রতিটা node এ দুটো জিনিস থাকে:

1. **Data** - যা store করতে চাই
2. **Pointer** - পরের node এর address

### Structure Definition:

```c
// Node এর structure define করা
struct Node {
    int data;              // Data part - যা store করব
    struct Node *next;     // Pointer part - পরের node এর address
};

// কেন struct Node *next?
// - struct Node: পরের node ও same type হবে
// - *next: এটা একটা pointer
// - next: pointer এর নাম
```

### Single Node Visualization:

```
┌─────────────────────┐
│      Node           │
├──────────┬──────────┤
│   Data   │   Next   │
│    10    │    →     │  → পরের node
└──────────┴──────────┘

Memory তে:
Address 1000:
┌──────────┬──────────┐
│    10    │   1500   │  (1500 = পরের node এর address)
└──────────┴──────────┘
```

### Creating a Node:

```c
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

int main() {
    // ১. Node এর জন্য memory allocate করা
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    // কী হলো:
    // - malloc: Memory allocate করো
    // - sizeof(struct Node): একটা Node এর size যতটুকু
    // - (struct Node*): Return type cast করা
    // - newNode: এই pointer এ address রাখা হলো
    
    // ২. Node এ data রাখা
    newNode->data = 10;
    // -> মানে: pointer দিয়ে member access
    // newNode->data == (*newNode).data
    
    // ৩. Next pointer NULL করা (এখনো কোনো next node নেই)
    newNode->next = NULL;
    
    // ৪. Print করা
    printf("Node এর data: %d\n", newNode->data);
    printf("Node এর next: %p\n", newNode->next);  // NULL
    
    // ৫. Memory free করা (important!)
    free(newNode);
    
    return 0;
}
```

### কী হচ্ছে Step by Step:

```
Step 1: malloc(sizeof(struct Node))
Memory allocate হলো:
┌──────────┬──────────┐
│    ?     │    ?     │  ← Garbage values
└──────────┴──────────┘
Address: 1000 (ধরি)
newNode = 1000

Step 2: newNode->data = 10
┌──────────┬──────────┐
│    10    │    ?     │
└──────────┴──────────┘

Step 3: newNode->next = NULL
┌──────────┬──────────┐
│    10    │   NULL   │
└──────────┴──────────┘

Step 4: free(newNode)
Memory release হলো, newNode এখন invalid
```

---

## Types of Linked Lists

### 1. Singly Linked List:

```
[Data|Next] → [Data|Next] → [Data|Next] → NULL

- একদিকে যাওয়া যায় (forward only)
- প্রতিটা node শুধু next রাখে
```

### 2. Doubly Linked List:

```
NULL ← [Prev|Data|Next] ↔ [Prev|Data|Next] ↔ [Prev|Data|Next] → NULL

- দুইদিকে যাওয়া যায় (forward এবং backward)
- প্রতিটা node prev এবং next দুটোই রাখে
```

### 3. Circular Linked List:

```
[Data|Next] → [Data|Next] → [Data|Next] ┐
  ↑                                      │
  └──────────────────────────────────────┘

- শেষ node প্রথম node এর দিকে point করে
- NULL নেই
```

আমরা **Singly Linked List** নিয়ে কাজ করব (সবচেয়ে common)।

---

## Singly Linked List Operations

### Basic Operations:

1. **Insert at Beginning** - শুরুতে যোগ করা
2. **Insert at End** - শেষে যোগ করা
3. **Insert at Position** - নির্দিষ্ট জায়গায় যোগ করা
4. **Delete from Beginning** - শুরু থেকে মুছে ফেলা
5. **Delete from End** - শেষ থেকে মুছে ফেলা
6. **Delete by Value** - নির্দিষ্ট value মুছে ফেলা
7. **Display** - সব nodes দেখানো
8. **Search** - নির্দিষ্ট value খোঁজা

---

### 1. Insert at Beginning:

```c
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

// শুরুতে insert করার function
void insertAtBeginning(struct Node **head, int value) {
    // কেন **head?
    // - head pointer change করতে হবে
    // - তাই head এর address লাগবে
    // - head এর address = pointer to pointer
    
    // ১. নতুন node তৈরি করা
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    // Memory allocate হলো
    
    // ২. Data রাখা
    newNode->data = value;
    
    // ৩. নতুন node এর next = পুরাতন head
    newNode->next = *head;
    // কেন *head?
    // - head হলো pointer to pointer
    // - *head হলো actual head pointer
    
    // ৪. Head update করা
    *head = newNode;
    // এখন নতুন node ই head
}

// List print করার function
void display(struct Node *head) {
    struct Node *temp = head;  // Traverse করার জন্য temporary pointer
    
    printf("List: ");
    while(temp != NULL) {
        printf("%d → ", temp->data);
        temp = temp->next;  // পরের node এ যাও
    }
    printf("NULL\n");
}

int main() {
    struct Node *head = NULL;  // শুরুতে list খালি
    
    printf("শুরুতে:\n");
    display(head);  // List: NULL
    
    insertAtBeginning(&head, 10);
    printf("\n10 insert এর পরে:\n");
    display(head);  // List: 10 → NULL
    
    insertAtBeginning(&head, 20);
    printf("\n20 insert এর পরে:\n");
    display(head);  // List: 20 → 10 → NULL
    
    insertAtBeginning(&head, 30);
    printf("\n30 insert এর পরে:\n");
    display(head);  // List: 30 → 20 → 10 → NULL
    
    return 0;
}
```

### কী হচ্ছে Visualization:

```
Initial: head = NULL
┌──────┐
│ head │ → NULL
└──────┘

After insertAtBeginning(&head, 10):

Step 1: নতুন node তৈরি
┌──────────┬──────────┐
│    10    │    ?     │  newNode
└──────────┴──────────┘

Step 2: newNode->next = *head (NULL)
┌──────────┬──────────┐
│    10    │   NULL   │  newNode
└──────────┴──────────┘

Step 3: *head = newNode
┌──────┐     ┌──────────┬──────────┐
│ head │ →   │    10    │   NULL   │
└──────┘     └──────────┴──────────┘

After insertAtBeginning(&head, 20):

Step 1: নতুন node তৈরি
┌──────────┬──────────┐
│    20    │    ?     │  newNode
└──────────┴──────────┘

Step 2: newNode->next = *head (10 এর address)
┌──────────┬──────────┐     ┌──────────┬──────────┐
│    20    │    →     │ →   │    10    │   NULL   │
└──────────┴──────────┘     └──────────┴──────────┘

Step 3: *head = newNode
┌──────┐     ┌──────────┬──────────┐     ┌──────────┬──────────┐
│ head │ →   │    20    │    →     │ →   │    10    │   NULL   │
└──────┘     └──────────┴──────────┘     └──────────┴──────────┘

Final: 30 → 20 → 10 → NULL
```

---

### 2. Insert at End:

```c
void insertAtEnd(struct Node **head, int value) {
    // ১. নতুন node তৈরি
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = NULL;  // শেষে যাবে, তাই next = NULL
    
    // ২. যদি list খালি হয়
    if(*head == NULL) {
        *head = newNode;  // নতুন node ই head
        return;
    }
    
    // ৩. শেষ node খুঁজে বের করা
    struct Node *temp = *head;
    while(temp->next != NULL) {
        temp = temp->next;  // শেষ পর্যন্ত যাও
    }
    // Loop শেষ হলে temp হলো শেষ node
    
    // ৪. শেষ node এর next = নতুন node
    temp->next = newNode;
}
```

### কী হচ্ছে:

```
Initial: 10 → 20 → NULL

insertAtEnd(&head, 30):

Step 1: নতুন node তৈরি
┌──────────┬──────────┐
│    30    │   NULL   │  newNode
└──────────┴──────────┘

Step 2: শেষ node খুঁজা
temp = head
temp = 10 → next != NULL, continue
temp = 20 → next == NULL, stop!
temp এখন 20 তে

Step 3: temp->next = newNode
┌──────────┬──────────┐     ┌──────────┬──────────┐     ┌──────────┬──────────┐
│    10    │    →     │ →   │    20    │    →     │ →   │    30    │   NULL   │
└──────────┴──────────┘     └──────────┴──────────┘     └──────────┴──────────┘

Final: 10 → 20 → 30 → NULL
```

---

### 3. Delete from Beginning:

```c
void deleteFromBeginning(struct Node **head) {
    // ১. যদি list খালি
    if(*head == NULL) {
        printf("List খালি! Delete করার কিছু নেই।\n");
        return;
    }
    
    // ২. মুছে ফেলার node save করা
    struct Node *temp = *head;
    
    // ৩. Head update করা
    *head = (*head)->next;
    // Head এখন দ্বিতীয় node
    
    // ৪. পুরাতন head free করা
    printf("%d deleted\n", temp->data);
    free(temp);
}
```

### কী হচ্ছে:

```
Initial: 10 → 20 → 30 → NULL

deleteFromBeginning(&head):

Step 1: temp = head (10)
┌──────┐     ┌──────────┬──────────┐
│ temp │ →   │    10    │    →     │
└──────┘     └──────────┴──────────┘

Step 2: head = head->next (20)
┌──────┐                 ┌──────────┬──────────┐
│ head │ →               │    20    │    →     │
└──────┘                 └──────────┴──────────┘

Step 3: free(temp)
10 এর node memory থেকে মুছে গেলো

Final: 20 → 30 → NULL
```

---

### 4. Search in List:

```c
int search(struct Node *head, int value) {
    struct Node *temp = head;
    int position = 0;
    
    // List traverse করা
    while(temp != NULL) {
        if(temp->data == value) {
            return position;  // পাওয়া গেছে!
        }
        temp = temp->next;
        position++;
    }
    
    return -1;  // পাওয়া যায়নি
}

// ব্যবহার:
int pos = search(head, 20);
if(pos != -1) {
    printf("20 পাওয়া গেছে position %d তে\n", pos);
} else {
    printf("20 পাওয়া যায়নি\n");
}
```

---

## Complete Implementation

এখন সব operations একসাথে:

```c
#include <stdio.h>
#include <stdlib.h>

// Node structure
struct Node {
    int data;
    struct Node *next;
};

// Function prototypes
void insertAtBeginning(struct Node **head, int value);
void insertAtEnd(struct Node **head, int value);
void insertAtPosition(struct Node **head, int value, int position);
void deleteFromBeginning(struct Node **head);
void deleteFromEnd(struct Node **head);
void deleteByValue(struct Node **head, int value);
void display(struct Node *head);
int search(struct Node *head, int value);
int getLength(struct Node *head);

int main() {
    struct Node *head = NULL;  // শুরুতে list খালি
    
    printf("=== Linked List Operations ===\n\n");
    
    // শুরুতে insert
    printf("1. শুরুতে insert:\n");
    insertAtBeginning(&head, 10);
    insertAtBeginning(&head, 20);
    insertAtBeginning(&head, 30);
    display(head);  // 30 → 20 → 10 → NULL
    
    // শেষে insert
    printf("\n2. শেষে insert:\n");
    insertAtEnd(&head, 40);
    insertAtEnd(&head, 50);
    display(head);  // 30 → 20 → 10 → 40 → 50 → NULL
    
    // নির্দিষ্ট position এ insert
    printf("\n3. Position 2 তে 25 insert:\n");
    insertAtPosition(&head, 25, 2);
    display(head);  // 30 → 20 → 25 → 10 → 40 → 50 → NULL
    
    // Length
    printf("\n4. List এর length: %d\n", getLength(head));
    
    // Search
    printf("\n5. 25 খোঁজা:\n");
    int pos = search(head, 25);
    if(pos != -1) {
        printf("25 পাওয়া গেছে position %d তে\n", pos);
    }
    
    // শুরু থেকে delete
    printf("\n6. শুরু থেকে delete:\n");
    deleteFromBeginning(&head);
    display(head);  // 20 → 25 → 10 → 40 → 50 → NULL
    
    // শেষ থেকে delete
    printf("\n7. শেষ থেকে delete:\n");
    deleteFromEnd(&head);
    display(head);  // 20 → 25 → 10 → 40 → NULL
    
    // নির্দিষ্ট value delete
    printf("\n8. 25 delete:\n");
    deleteByValue(&head, 25);
    display(head);  // 20 → 10 → 40 → NULL
    
    return 0;
}

// শুরুতে insert
void insertAtBeginning(struct Node **head, int value) {
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = *head;
    *head = newNode;
    printf("%d inserted at beginning\n", value);
}

// শেষে insert
void insertAtEnd(struct Node **head, int value) {
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = NULL;
    
    if(*head == NULL) {
        *head = newNode;
        printf("%d inserted at end (first node)\n", value);
        return;
    }
    
    struct Node *temp = *head;
    while(temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
    printf("%d inserted at end\n", value);
}

// নির্দিষ্ট position এ insert
void insertAtPosition(struct Node **head, int value, int position) {
    // Position 0 মানে beginning
    if(position == 0) {
        insertAtBeginning(head, value);
        return;
    }
    
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    
    struct Node *temp = *head;
    // Position-1 পর্যন্ত যাও
    for(int i = 0; i < position - 1 && temp != NULL; i++) {
        temp = temp->next;
    }
    
    if(temp == NULL) {
        printf("Invalid position!\n");
        free(newNode);
        return;
    }
    
    newNode->next = temp->next;
    temp->next = newNode;
    printf("%d inserted at position %d\n", value, position);
}

// শুরু থেকে delete
void deleteFromBeginning(struct Node **head) {
    if(*head == NULL) {
        printf("List খালি!\n");
        return;
    }
    
    struct Node *temp = *head;
    *head = (*head)->next;
    printf("%d deleted from beginning\n", temp->data);
    free(temp);
}

// শেষ থেকে delete
void deleteFromEnd(struct Node **head) {
    if(*head == NULL) {
        printf("List খালি!\n");
        return;
    }
    
    // যদি শুধু একটা node থাকে
    if((*head)->next == NULL) {
        printf("%d deleted from end\n", (*head)->data);
        free(*head);
        *head = NULL;
        return;
    }
    
    // শেষ থেকে দ্বিতীয় node খুঁজা
    struct Node *temp = *head;
    while(temp->next->next != NULL) {
        temp = temp->next;
    }
    
    printf("%d deleted from end\n", temp->next->data);
    free(temp->next);
    temp->next = NULL;
}

// নির্দিষ্ট value delete
void deleteByValue(struct Node **head, int value) {
    if(*head == NULL) {
        printf("List খালি!\n");
        return;
    }
    
    // যদি first node ই delete করতে হয়
    if((*head)->data == value) {
        deleteFromBeginning(head);
        return;
    }
    
    struct Node *temp = *head;
    // Value খুঁজা
    while(temp->next != NULL && temp->next->data != value) {
        temp = temp->next;
    }
    
    if(temp->next == NULL) {
        printf("%d পাওয়া যায়নি!\n", value);
        return;
    }
    
    struct Node *toDelete = temp->next;
    temp->next = temp->next->next;
    printf("%d deleted\n", value);
    free(toDelete);
}

// Display
void display(struct Node *head) {
    if(head == NULL) {
        printf("List: NULL\n");
        return;
    }
    
    struct Node *temp = head;
    printf("List: ");
    while(temp != NULL) {
        printf("%d → ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

// Search
int search(struct Node *head, int value) {
    struct Node *temp = head;
    int position = 0;
    
    while(temp != NULL) {
        if(temp->data == value) {
            return position;
        }
        temp = temp->next;
        position++;
    }
    
    return -1;
}

// Length
int getLength(struct Node *head) {
    int count = 0;
    struct Node *temp = head;
    
    while(temp != NULL) {
        count++;
        temp = temp->next;
    }
    
    return count;
}
```

---

## Memory Management

### Important Points:

```c
// ✅ সঠিক - Memory allocate করা
struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));

// ✅ সঠিক - ব্যবহার শেষে free করা
free(newNode);

// ❌ ভুল - Free না করা (Memory leak!)
struct Node *node = (struct Node*)malloc(sizeof(struct Node));
// ... ব্যবহার করা ...
// free() করা হয়নি! Memory leak!

// ❌ ভুল - Free এর পরে access করা
free(node);
printf("%d", node->data);  // Dangerous!
```

### Entire List Free করা:

```c
void freeList(struct Node **head) {
    struct Node *temp;
    
    while(*head != NULL) {
        temp = *head;           // Current node save
        *head = (*head)->next;  // Head move করা
        free(temp);             // Current node free করা
    }
    
    printf("সম্পূর্ণ list free করা হয়েছে\n");
}
```

---

## Common Problems

### 1. Reverse a Linked List:

```c
void reverse(struct Node **head) {
    struct Node *prev = NULL;
    struct Node *current = *head;
    struct Node *next = NULL;
    
    while(current != NULL) {
        next = current->next;    // পরের node save
        current->next = prev;    // Link reverse করা
        prev = current;          // prev এগিয়ে নেওয়া
        current = next;          // current এগিয়ে নেওয়া
    }
    
    *head = prev;  // নতুন head
}
```

### 2. Find Middle Element:

```c
int findMiddle(struct Node *head) {
    struct Node *slow = head;
    struct Node *fast = head;
    
    // Fast 2 step, slow 1 step
    while(fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
    }
    
    // Fast শেষে পৌঁছালে slow middle এ
    return slow->data;
}
```

### 3. Detect Loop:

```c
int hasLoop(struct Node *head) {
    struct Node *slow = head;
    struct Node *fast = head;
    
    while(fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        
        if(slow == fast) {
            return 1;  // Loop আছে!
        }
    }
    
    return 0;  // Loop নেই
}
```

---

## Summary

### Key Points:

- ✅ Linked List = Nodes এর chain
- ✅ Node = Data + Pointer
- ✅ Dynamic size - যতটুকু চাই
- ✅ Easy insertion/deletion
- ✅ Pointer ভালো বুঝতে হবে
- ✅ malloc/free সঠিকভাবে ব্যবহার করতে হবে

### Advantages:

- ✅ Dynamic size
- ✅ Easy insertion/deletion
- ✅ No memory waste
- ✅ Flexible

### Disadvantages:

- ❌ No random access
- ❌ Extra memory for pointers
- ❌ Not cache friendly

### Next Steps:

- Doubly Linked List
- Circular Linked List
- Stack using Linked List
- Queue using Linked List

**Linked List = Foundation of Data Structures!** 🚀
