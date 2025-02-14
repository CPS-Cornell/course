# A Gentle Introduction to Asynchronous Programming in Python

## 1. What Is Asynchronous Programming?

Imagine you have a single cook (a single CPU core) in a kitchen. If your cook works on tasks **sequentially**, they must finish one dish (task) entirely before starting the next. If there’s a moment of waiting—like a sauce simmering—they still spend that “waiting” time doing nothing else (in code terms, blocking), even though it doesn’t require active attention.

**Asynchronous programming** is like having the cook pick up the next dish whenever a current dish is waiting for something else (e.g., water to boil). The cook isn’t magically duplicating themselves; they’re just switching tasks efficiently when possible. This model allows your code to process multiple tasks cooperatively, **interleaving** them in a single thread of execution.

### Why Use Asynchronous Programming?
- **Concurrency**: If your program frequently waits on I/O (network requests, file reads/writes, etc.), asynchronous code can run these operations in parallel, improving responsiveness.
- **Efficiency**: Minimizes wasted time while waiting for slow operations.
- **Scalability**: Handling multiple simultaneous connections or tasks is easier without running multiple OS threads or processes (though threads and processes also have their place).

---

## 2. The `asyncio` Library

In modern Python (**3.8+**), the recommended approach to asynchronous programming is with the **`asyncio`** module. It introduces:
- **Coroutines** (created with `async def`).
- An **event loop** (managed by functions like `asyncio.run()`).
- Keywords like **`await`** for pausing/resuming coroutines.

### The Event Loop

Think of the **event loop** as the master scheduler that juggles all asynchronous tasks. It’s a loop that:
1. Checks each task to see if it’s ready to do work.
2. Hands control to tasks that can proceed.
3. Suspends tasks that need to wait for an I/O event (like network data).
4. Moves on to the next task.

This all happens under the hood, making asynchronous tasks feel somewhat like writing normal sequential code, but you have to follow certain syntax rules (using `async def` and `await`).

---

## 3. Syntax Rules for Async Functions

### `async def`

An **async function** (coroutine) must start with:

```python
async def my_coroutine():
    ...
```

vs. a normal function:

```python
def my_normal_function():
    ...
```

**When do you use `async def`?**  
- When you want the function to be awaitable (i.e., you can use the `await` keyword inside it).
- When the function performs asynchronous I/O operations (or depends on other async functions).

### `await`

The **`await`** keyword appears *inside* `async def` functions. It means:

> “Pause this function here, let other tasks run, and come back to me when the awaited operation is complete.”

For example:

```python
async def fetch_data():
    data = await some_network_operation()
    return data
```

- You can only use `await` **inside** an `async def` function, *not* in a normal function.
- You typically await **other async functions** or special awaitable objects (like tasks and futures).

---

## 4. A Simple Toy Example

### Example: Two Coroutines, One Event Loop

```python
import asyncio

async def print_numbers(name, delay):
    """Print three numbers with a delay between each."""
    for i in range(1, 4):
        print(f"{name} -> {i}")
        await asyncio.sleep(delay)

async def main():
    task1 = asyncio.create_task(print_numbers("Task1", 1))
    task2 = asyncio.create_task(print_numbers("Task2", 0.5))

    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. UART Communication and Asynchronous Programming

### What Is UART?
UART (**Universal Asynchronous Receiver/Transmitter**) is a serial communication protocol used to send and receive data between devices. It is **asynchronous** in nature, meaning that it does not use a shared clock between the sender and receiver. Instead, both devices agree on a predefined baud rate (e.g., **115200 baud**) and transmit bits accordingly.

### Why Use Asynchronous Programming for UART?
If you use **synchronous (blocking) code** for UART, the program will **pause execution** while waiting for data to arrive, making it inefficient for real-time applications. Instead, asynchronous programming allows the CPU to **listen for incoming data while doing other tasks**.

### Example: Async UART Communication with `asyncio`
```python
import asyncio
import serial_asyncio

class SerialReader(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("Serial connection established")

    def data_received(self, data):
        print(f"Received: {data.decode().strip()}")

async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await serial_asyncio.create_serial_connection(
        loop, SerialReader, '/dev/ttyUSB0', baudrate=115200
    )

    await asyncio.sleep(9999)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 6. Asyncio in MicroPython on Raspberry Pi Pico

### MicroPython and Asynchronous Programming
MicroPython is a lightweight version of Python designed for **microcontrollers**. Unlike full Python, it has a **stripped-down implementation** of `asyncio` designed for embedded systems.

### Supported Features in MicroPython
MicroPython on the **Raspberry Pi Pico** (or similar boards) provides **partial** support for `asyncio`. The **core module** is called `uasyncio`.

### Example: Asynchronous UART on Raspberry Pi Pico
```python
import uasyncio as asyncio
from machine import UART, Pin

uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

async def read_uart():
    while True:
        if uart.any():
            data = uart.read().decode()
            print(f"Received: {data.strip()}")
        await asyncio.sleep(0.1)

async def blink_led():
    led = Pin(25, Pin.OUT)
    while True:
        led.toggle()
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(read_uart(), blink_led())

asyncio.run(main())
```

---

## 7. Key Takeaways

1. **Async programming is ideal for waiting tasks** (e.g., network, UART, I/O).
2. **UART communication benefits from async** because data arrives at unpredictable times.
3. **MicroPython's `uasyncio` provides async support on microcontrollers** but has some limitations.
4. **Use async where I/O tasks might block execution**—like reading sensors while keeping an LED blinking.

---

## 8. Next Steps

- **Experiment with UART communication** using `asyncio` and MicroPython.
- **Try running multiple async tasks** on the Raspberry Pi Pico.
- **Explore real-world applications** (e.g., Wi-Fi data logging, GPS tracking, async web servers).

By understanding **asynchronous execution** on both **full Python** and **MicroPython**, you can build **responsive, efficient embedded systems** that multitask effectively. 🚀


