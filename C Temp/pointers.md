# C Programming - Pointers (পয়েন্টার)

## সূচিপত্র

1. [পরিচিতি](#পরিচিতি)
2. [Pointer কী এবং কেন?](#pointer-কী-এবং-কেন)
3. [Memory এবং Address](#memory-এবং-address)
4. [Pointer Declaration](#pointer-declaration)
5. [Pointer Operators](#pointer-operators)
6. [Pointer Arithmetic](#pointer-arithmetic)
7. [Pointer এবং Arrays](#pointer-এবং-arrays)
8. [Pointer এবং Functions](#pointer-এবং-functions)
9. [Double Pointers](#double-pointers)
10. [Common Mistakes](#common-mistakes)

---

## পরিচিতি

Pointer হলো C Programming এর সবচেয়ে powerful এবং গুরুত্বপূর্ণ concept। এটা বুঝলে Linked List, Trees, Dynamic Memory সব সহজ হয়ে যাবে।

### কেন Pointer শিখব?

- ✅ **Linked List** বুঝতে হলে pointer অবশ্যই লাগবে
- ✅ **Dynamic Memory Allocation** করতে হলে pointer লাগবে
- ✅ **Function এ বড় data pass** করতে efficient
- ✅ **Data Structures** (Tree, Graph) বানাতে লাগবে

---

## Pointer কী এবং কেন?

### Pointer কী?

**সহজ ভাষায়:** Pointer হলো একটা variable যা অন্য variable এর **address** (ঠিকানা) রাখে।

```
Normal Variable = মান রাখে
Pointer = ঠিকানা রাখে
```

### Real-World উদাহরণ:

```
আপনার বাড়ি = Variable (যেখানে আপনি থাকেন)
আপনার বাড়ির ঠিকানা = Pointer (বাড়ি খুঁজে পেতে)

কেউ যদি আপনার বাড়িতে যেতে চায়:
- সরাসরি বাড়ি নিয়ে যেতে পারবে না (বড়, ভারী)
- ঠিকানা দিলেই হবে (ছোট, হালকা)
- ঠিকানা দিয়ে বাড়ি খুঁজে পাবে

তেমনি:
- বড় data সরাসরি pass করা কঠিন
- Address (pointer) pass করা সহজ
- Address দিয়ে data access করা যায়
```

---

## Memory এবং Address

### Computer Memory কীভাবে কাজ করে?

Computer এর memory হলো অনেকগুলো boxes এর মতো। প্রতিটা box এর একটা unique address আছে।

```
Memory Visualization:

Address:    Value:
┌─────────┬─────────┐
│  1000   │    ?    │  ← খালি
├─────────┼─────────┤
│  1001   │    ?    │  ← খালি
├─────────┼─────────┤
│  1002   │   10    │  ← int num = 10;
├─────────┼─────────┤
│  1003   │    ?    │  ← খালি
├─────────┼─────────┤
│  1004   │  1002   │  ← int *ptr = &num; (num এর address রাখছে)
├─────────┼─────────┤
│  1005   │    ?    │  ← খালি
└─────────┴─────────┘
```

### কী হচ্ছে এখানে:

```c
int num = 10;        // Address 1002 তে 10 রাখা হলো
int *ptr = &num;     // Address 1004 তে 1002 রাখা হলো

// num এর:
// - Value: 10
// - Address: 1002

// ptr এর:
// - Value: 1002 (num এর address)
// - Address: 1004
```

---

## Pointer Declaration

### Syntax:

```c
datatype *pointer_name;
```

### Examples:

```c
// Integer pointer ঘোষণা
int *ptr;
// পড়ুন: "ptr হলো একটা pointer যা integer এর address রাখবে"

// Character pointer
char *cptr;
// পড়ুন: "cptr হলো একটা pointer যা character এর address রাখবে"

// Float pointer
float *fptr;
// পড়ুন: "fptr হলো একটা pointer যা float এর address রাখবে"
```

### কেন * চিহ্ন?

```c
int *ptr;

// * মানে: "এটা একটা pointer"
// int মানে: "এটা integer এর address রাখবে"
// ptr মানে: "pointer এর নাম ptr"
```

### Complete Example:

```c
#include <stdio.h>

int main() {
    // ১. সাধারণ variable ঘোষণা এবং initialize
    int num = 10;
    // কী হলো: Memory তে একটা জায়গা নেওয়া হলো
    // কোথায়: ধরি address 1002
    // কী রাখা হলো: 10
    
    // ২. Pointer ঘোষণা
    int *ptr;
    // কী হলো: আরেকটা variable তৈরি হলো
    // কোথায়: ধরি address 1004
    // কী রাখবে: Integer এর address
    
    // ৩. Pointer এ address assign করা
    ptr = &num;
    // & মানে: "address of" (এর ঠিকানা)
    // কী হলো: num এর address (1002) ptr এ রাখা হলো
    
    // ৪. Print করা
    printf("num এর value: %d\n", num);           // 10
    printf("num এর address: %p\n", &num);        // 1002 (example)
    printf("ptr এর value: %p\n", ptr);           // 1002 (num এর address)
    printf("ptr যেখানে point করছে সেই value: %d\n", *ptr);  // 10
    
    return 0;
}
```

### Output ব্যাখ্যা:

```
num এর value: 10
↑ সরাসরি num এর মান

num এর address: 0x7ffd5c7e4a0c
↑ num কোথায় আছে (memory address)

ptr এর value: 0x7ffd5c7e4a0c
↑ ptr কী রাখছে (num এর address)

ptr যেখানে point করছে সেই value: 10
↑ ptr দিয়ে num এর মান access করা
```

---

## Pointer Operators

### দুটো main operators:

#### 1. & (Address-of Operator):

```c
int num = 10;
int *ptr = &num;  // & দিয়ে num এর address নেওয়া

// & মানে: "এর ঠিকানা দাও"
```

**কী হচ্ছে:**

```
&num
↓
"num variable টা memory এর কোথায় আছে সেই address দাও"
↓
1002 (example address)
```

#### 2. * (Dereference Operator):

```c
int num = 10;
int *ptr = &num;
int value = *ptr;  // * দিয়ে ptr যেখানে point করছে সেই value নেওয়া

// * মানে: "যেখানে point করছো সেখানের value দাও"
```

**কী হচ্ছে:**

```
*ptr
↓
"ptr যে address রাখছে (1002), সেখানে কী আছে?"
↓
10 (num এর value)
```

### Complete Example:

```c
#include <stdio.h>

int main() {
    int num = 25;
    int *ptr = &num;
    
    // বিভিন্ন উপায়ে access করা
    
    // ১. সরাসরি num
    printf("সরাসরি num: %d\n", num);  // 25
    
    // ২. Pointer দিয়ে
    printf("Pointer দিয়ে: %d\n", *ptr);  // 25
    
    // ৩. Pointer দিয়ে value change করা
    *ptr = 50;
    // কী হলো: ptr যেখানে point করছে (num), সেখানে 50 রাখা হলো
    
    printf("Change এর পরে num: %d\n", num);  // 50
    printf("Change এর পরে *ptr: %d\n", *ptr);  // 50
    
    // ৪. Address দেখা
    printf("\nnum এর address: %p\n", &num);
    printf("ptr এ কী আছে: %p\n", ptr);
    printf("ptr নিজে কোথায়: %p\n", &ptr);
    
    return 0;
}
```

### কী হচ্ছে Step by Step:

```
Step 1: int num = 25;
Memory:
[1002] → 25

Step 2: int *ptr = &num;
Memory:
[1002] → 25    (num)
[1004] → 1002  (ptr, num এর address রাখছে)

Step 3: *ptr = 50;
কী হলো:
- ptr এ আছে 1002
- *ptr মানে address 1002 এ যাও
- সেখানে 50 রাখো

Memory:
[1002] → 50    (num, changed!)
[1004] → 1002  (ptr, same)

Result:
- num = 50 (changed)
- *ptr = 50 (same as num)
```

---

## Pointer Arithmetic

Pointer এ arithmetic operations করা যায়!

### কেন Pointer Arithmetic?

Array traverse করতে, memory তে এক জায়গা থেকে আরেক জায়গায় যেতে।

### Operations:

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *ptr = arr;  // Array এর first element এর address
    
    // কী হলো:
    // arr[0] এর address = 1000 (ধরি)
    // ptr = 1000
    
    printf("ptr এর value: %p\n", ptr);           // 1000
    printf("ptr এ কী আছে: %d\n", *ptr);          // 10
    
    // Pointer increment
    ptr++;
    // কী হলো: ptr = ptr + 1
    // কিন্তু 1000 + 1 = 1001 না!
    // Integer size = 4 bytes
    // তাই: 1000 + (1 * 4) = 1004
    
    printf("\nIncrement এর পরে:\n");
    printf("ptr এর value: %p\n", ptr);           // 1004
    printf("ptr এ কী আছে: %d\n", *ptr);          // 20
    
    // আরো increment
    ptr++;  // 1008 তে যাবে
    printf("\nআরো increment:\n");
    printf("ptr এ কী আছে: %d\n", *ptr);          // 30
    
    // Pointer arithmetic
    ptr = ptr + 2;  // 2টা element এগিয়ে যাও
    // 1008 + (2 * 4) = 1016
    printf("\n2 element এগিয়ে:\n");
    printf("ptr এ কী আছে: %d\n", *ptr);          // 50
    
    return 0;
}
```

### Memory Layout:

```
Array: {10, 20, 30, 40, 50}

Memory:
Address:  Value:  Element:
┌─────────┬───────┬─────────┐
│  1000   │  10   │  arr[0] │ ← ptr initially
├─────────┼───────┼─────────┤
│  1004   │  20   │  arr[1] │ ← ptr++ (ptr এখানে)
├─────────┼───────┼─────────┤
│  1008   │  30   │  arr[2] │ ← ptr++ (ptr এখানে)
├─────────┼───────┼─────────┤
│  1012   │  40   │  arr[3] │
├─────────┼───────┼─────────┤
│  1016   │  50   │  arr[4] │ ← ptr + 2 (ptr এখানে)
└─────────┴───────┴─────────┘

কেন 4 bytes gap?
- int size = 4 bytes
- তাই প্রতিটা element 4 bytes দূরে
```

---

## Pointer এবং Arrays

### Array এবং Pointer এর সম্পর্ক:

```c
int arr[] = {10, 20, 30};
int *ptr = arr;

// এই দুটো same:
arr[0]  ==  *ptr
arr[1]  ==  *(ptr + 1)
arr[2]  ==  *(ptr + 2)

// এবং এই দুটোও same:
&arr[0]  ==  ptr
&arr[1]  ==  ptr + 1
&arr[2]  ==  ptr + 2
```

### Complete Example:

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *ptr = arr;  // arr মানেই first element এর address
    
    printf("Array traverse - Method 1 (Array notation):\n");
    for(int i = 0; i < 5; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    
    printf("\nArray traverse - Method 2 (Pointer notation):\n");
    for(int i = 0; i < 5; i++) {
        printf("*(ptr + %d) = %d\n", i, *(ptr + i));
        // কী হচ্ছে:
        // i=0: *(ptr + 0) = *ptr = arr[0] = 10
        // i=1: *(ptr + 1) = arr[1] = 20
        // i=2: *(ptr + 2) = arr[2] = 30
    }
    
    printf("\nArray traverse - Method 3 (Pointer increment):\n");
    int *temp = arr;  // নতুন pointer, arr change হবে না
    for(int i = 0; i < 5; i++) {
        printf("*temp = %d\n", *temp);
        temp++;  // পরের element এ যাও
        // কী হচ্ছে:
        // প্রথমে: temp → arr[0]
        // temp++ → arr[1]
        // temp++ → arr[2]
    }
    
    return 0;
}
```

---

## Pointer এবং Functions

### কেন Function এ Pointer পাঠাই?

**সমস্যা:** Normal variable pass করলে copy হয়, original change হয় না।

```c
#include <stdio.h>

// এটা কাজ করবে না!
void increment_wrong(int num) {
    num = num + 1;  // শুধু copy change হবে
}

// এটা কাজ করবে!
void increment_right(int *ptr) {
    *ptr = *ptr + 1;  // Original change হবে
}

int main() {
    int value = 10;
    
    printf("শুরুতে: %d\n", value);  // 10
    
    increment_wrong(value);
    printf("Wrong function এর পরে: %d\n", value);  // 10 (same!)
    
    increment_right(&value);  // Address পাঠাচ্ছি
    printf("Right function এর পরে: %d\n", value);  // 11 (changed!)
    
    return 0;
}
```

### কী হচ্ছে:

```
increment_wrong(value):
┌─────────────────┐
│ main()          │
│ value = 10      │ ← Original
│ [1000] → 10     │
└─────────────────┘
        ↓ copy
┌─────────────────┐
│ increment_wrong │
│ num = 10        │ ← Copy
│ [2000] → 10     │
│ num = 11        │ ← Copy changed
│ [2000] → 11     │
└─────────────────┘
        ↓ function শেষ, copy মুছে গেলো
┌─────────────────┐
│ main()          │
│ value = 10      │ ← Original unchanged!
└─────────────────┘

increment_right(&value):
┌─────────────────┐
│ main()          │
│ value = 10      │
│ [1000] → 10     │
└─────────────────┘
        ↓ address পাঠানো
┌─────────────────┐
│ increment_right │
│ ptr = 1000      │ ← Address পেলো
│ *ptr = 11       │ ← Address 1000 এ গিয়ে change করলো
└─────────────────┘
        ↓
┌─────────────────┐
│ main()          │
│ value = 11      │ ← Original changed!
│ [1000] → 11     │
└─────────────────┘
```

### Swap Function Example:

```c
#include <stdio.h>

// দুটো number swap করা
void swap(int *a, int *b) {
    // a এবং b হলো address
    // *a এবং *b হলো actual values
    
    int temp = *a;  // temp = a এর value
    *a = *b;        // a তে b এর value রাখো
    *b = temp;      // b তে temp (আগের a) রাখো
}

int main() {
    int x = 5, y = 10;
    
    printf("আগে: x = %d, y = %d\n", x, y);
    
    swap(&x, &y);  // x এবং y এর address পাঠানো
    
    printf("পরে: x = %d, y = %d\n", x, y);
    
    return 0;
}

// Output:
// আগে: x = 5, y = 10
// পরে: x = 10, y = 5
```

---

## Double Pointers

### Pointer to Pointer:

```c
int num = 10;
int *ptr = &num;      // ptr → num এর address
int **pptr = &ptr;    // pptr → ptr এর address

// pptr হলো pointer to pointer
```

### Visualization:

```
Memory:
┌─────────┬─────────┐
│  1000   │   10    │  ← num
├─────────┼─────────┤
│  1004   │  1000   │  ← ptr (num এর address)
├─────────┼─────────┤
│  1008   │  1004   │  ← pptr (ptr এর address)
└─────────┴─────────┘

Access:
num     → 10
*ptr    → 10  (ptr দিয়ে num access)
**pptr  → 10  (pptr → ptr → num)
```

### Example:

```c
#include <stdio.h>

int main() {
    int num = 100;
    int *ptr = &num;
    int **pptr = &ptr;
    
    printf("num এর value: %d\n", num);          // 100
    printf("*ptr: %d\n", *ptr);                  // 100
    printf("**pptr: %d\n", **pptr);              // 100
    
    // Change করা
    **pptr = 200;
    // কী হলো:
    // pptr → ptr এর address
    // *pptr → ptr এর value (num এর address)
    // **pptr → num এর value
    // **pptr = 200 → num = 200
    
    printf("\nChange এর পরে:\n");
    printf("num: %d\n", num);                    // 200
    printf("*ptr: %d\n", *ptr);                  // 200
    printf("**pptr: %d\n", **pptr);              // 200
    
    return 0;
}
```

---

## Common Mistakes

### 1. Uninitialized Pointer:

```c
// ❌ ভুল - Dangerous!
int *ptr;
*ptr = 10;  // ptr কোথায় point করছে জানি না!

// ✅ সঠিক
int num;
int *ptr = &num;
*ptr = 10;  // এখন safe
```

### 2. NULL Pointer Dereference:

```c
// ❌ ভুল
int *ptr = NULL;
*ptr = 10;  // Crash! NULL এ কিছু রাখা যায় না

// ✅ সঠিক
int *ptr = NULL;
if(ptr != NULL) {
    *ptr = 10;
}
```

### 3. Dangling Pointer:

```c
// ❌ ভুল
int *ptr;
{
    int num = 10;
    ptr = &num;
}  // num এখানে destroy হয়ে গেলো
*ptr = 20;  // Dangerous! num আর নেই

// ✅ সঠিক
int num = 10;
int *ptr = &num;
*ptr = 20;  // Safe
```

---

## Summary

### Key Points:

- ✅ Pointer = Address রাখে
- ✅ `&` = Address নেওয়ার জন্য
- ✅ `*` = Value access করার জন্য
- ✅ Pointer arithmetic = Memory traverse
- ✅ Function এ pointer = Original change
- ✅ Array = Pointer এর মতো
- ✅ Double pointer = Pointer এর pointer

### Next Step:

এখন Pointer বুঝে গেছেন! পরের file **Linked List** এ এই pointer ব্যবহার করে dynamic data structure বানাবো।

**Pointer = Linked List এর foundation!** 🚀
