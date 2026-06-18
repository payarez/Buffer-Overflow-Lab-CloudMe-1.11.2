# Buffer-Overflow-Lab-CloudMe-1.11.2
Hands-on cybersecurity lab focused on buffer overflow analysis and exploitation in a controlled environment.

## Overview

This repository documents a hands-on cybersecurity laboratory focused on understanding and analyzing a classic Buffer Overflow vulnerability in a controlled and isolated environment.

The objective of this lab was to learn the methodology used to identify, analyze, and validate a stack-based buffer overflow vulnerability using debugging and reverse engineering techniques.

> This project was conducted exclusively for educational purposes in a virtualized laboratory environment.

---

## Learning Objectives

- Understand the fundamentals of stack-based buffer overflows.
- Perform vulnerability analysis in a controlled environment.
- Learn how memory corruption affects program execution.
- Gain experience using debugging tools.
- Understand exploit development methodology.
- Study common mitigation techniques.

---

## Lab Environment

| Component | Version |
|------------|-----------|
| Victim System | Windows 10 x86 |
| Attacker System | Kali Linux x64 |
| Vulnerable Application | CloudMe 1.11.2 |
| Debugger | Immunity Debugger |
| Analysis Plugin | mona.py |
| Scripting Language | Python |
| Virtualization | Virtual Machine |

---

## Using Immunity Debugger

A virtualized laboratory environment was configured to safely perform the analysis. The target application, CloudMe v1.11.2, was deployed on a Windows 10 virtual machine, while the analysis and testing activities were conducted from a separate Kali Linux system.

Immunity Debugger and Mona.py were used to monitor the application's behavior during the different stages of the assessment and to inspect memory structures when crashes occurred.

- To begin the analysis, Immunity Debugger was launched on the target Windows machine. The CloudMe process was then attached by navigating to **File → Attach** and selecting the running CloudMe process from the available list.

- Once attached, the application could be monitored in real time, allowing inspection of memory regions, processor registers, loaded modules, and execution flow.

- During fuzzing and subsequent testing phases, Immunity Debugger automatically paused execution whenever the application crashed, making it possible to investigate the cause of the memory corruption.

- To resume program execution after attaching to the process, the **Run** button (play icon) located in the toolbar was used.

- Since the application terminated after each crash, CloudMe was restarted and reattached to Immunity Debugger before continuing with additional tests.

- Particular attention was given to the CPU window, where the processor registers are displayed. The **EIP (Extended Instruction Pointer)** register was monitored to verify control over program execution, while the **ESP (Extended Stack Pointer)** register was analyzed to understand stack behavior during the different stages of the assessment.

![Environment Setup](images/Picture1.png)

---

## Methodology

### Phase 1: Fuzzing and Crash Identification

A fuzzing process was performed by sending progressively larger inputs to the application. The purpose of this phase was to observe how the service handled unexpected or oversized data and determine whether memory corruption conditions could be triggered.

```Python
import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

size = 100

while size < 3000:

    print("\n[+] Sending {} bytes".format(size))

    raw_input("[*] Press Enter to continue...")

    try:
        payload = "A" * size

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((TARGET_IP, TARGET_PORT))
        client.send(payload)
        client.close()

        size += 100

    except:
        print("[!] Crash around {} bytes".format(size))
        break

```

![Attaching Process](images/1_immunityAttach.png)

After multiple iterations, the application crashed when processing an oversized input, indicating the presence of a potential buffer overflow vulnerability. The debugger confirmed that critical memory structures were being affected during the crash.

![Fuzzing Process](images/1_crash1200.png)

#### Evidence

![Fuzzing Result](images/1_errorMessage.png)

---

### Phase 3: Offset Calculation

A cyclic pattern was generated and injected into the application to determine the exact offset required to overwrite the instruction pointer.

#### Objectives

- Determine EIP control.
- Identify the precise overwrite location.

#### Evidence

![Offset Calculation](images/offset.png)

---

### Phase 4: EIP Control Verification

A controlled value was inserted at the identified offset to verify successful control over the program execution flow.

#### Objectives

- Confirm EIP overwrite.
- Validate previous calculations.

#### Evidence

![EIP Control](images/eip-control.png)

---

### Phase 5: Bad Character Analysis

Input validation testing was conducted to identify characters that could interfere with payload execution.

#### Objectives

- Identify problematic bytes.
- Build a valid character set.

#### Evidence

![Bad Characters Analysis](images/badchars.png)

---

### Phase 6: Memory Analysis

A suitable instruction sequence was located within the process memory to redirect execution flow.

#### Objectives

- Analyze loaded modules.
- Locate executable memory regions.
- Understand control flow redirection.

#### Evidence

![Memory Analysis](images/memory-analysis.png)

---

### Phase 7: Final Validation

The laboratory concluded with the validation of the complete vulnerability analysis process in the controlled environment.

#### Objectives

- Verify reproducibility.
- Confirm understanding of exploitation workflow.

#### Evidence

![Final Validation](images/final-validation.png)

---
