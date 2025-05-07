# Understanding Hardware Event Detection: Polling vs. Interrupts

This document explains two fundamental approaches to detecting hardware events (like button presses) in embedded systems: polling and interrupts. The examples use MicroPython on a microcontroller.

## Polling Approach ([`push_button_polling.py`](push_button_polling.py))

In the polling approach, the code continuously checks (polls) the state of the input to detect changes.

### How push_button_polling.py Works:

1. **Setup**: Configures GPIO pin 22 as an input with a pull-up resistor.
2. **Main Loop**: Continuously checks the button state in an infinite loop.
3. **Event Detection**: When the button is pressed (pin value becomes 0), it increments a counter and displays a message.
4. **Debouncing**: Implements a simple time delay (0.2 seconds) to avoid counting multiple presses from a single physical button press.
5. **CPU Usage**: Includes a small delay (0.01 seconds) to reduce CPU usage during polling.

### Characteristics of Polling:

- **Simple to implement**: Just check the state repeatedly in a loop.
- **Predictable timing**: The button is checked at regular intervals.
- **CPU intensive**: The CPU must continuously run the checking code.
- **Can miss events**: If the event occurs and ends between checks, it will be missed.
- **May introduce latency**: The system only responds when the next check occurs.

## Interrupt Approach ([`push_button_interrupt.py`](push_button_interrupt.py))

In the interrupt approach, the hardware automatically notifies the CPU when an event occurs, triggering a specific function.

### How push_button_interrupt.py Works:

1. **Setup**: Configures GPIO pin 22 as an input with a pull-up resistor.
2. **Interrupt Registration**: Sets up an interrupt handler (`button_pressed`) to be called on the falling edge (when button is pressed).
3. **Event Handling**: When the button is pressed, the hardware automatically triggers the handler function.
4. **Debouncing**: Uses time-based debouncing by tracking the last press time and ignoring events that occur within 100ms.
5. **Main Loop**: Is free to do other tasks while waiting for button presses.

### Characteristics of Interrupts:

- **More efficient**: CPU only responds when events occur, not wasting cycles checking.
- **Immediate response**: The handler is called as soon as the event occurs.
- **Won't miss events**: Even brief events will trigger the interrupt (though debouncing may filter some out).
- **More complex**: Requires understanding of interrupt systems and careful handling of shared resources.
- **Can interrupt critical code**: Need to consider what happens if an interrupt occurs during sensitive operations.

## Comparing Approaches

| Aspect | Polling | Interrupts |
|--------|---------|------------|
| CPU Usage | Higher (constantly checking) | Lower (responds only when needed) |
| Response Time | Variable (depends on polling frequency) | Immediate |
| Event Detection | May miss brief events | Catches all events (subject to debouncing) |
| Complexity | Simpler to implement and understand | More complex, requires careful design |
| Multitasking | Difficult (polling loop dominates CPU time) | Easier (main program free to do other work) |
| Timing Precision | Less precise (limited by polling interval) | More precise (responds at exact event time) |

## When to Use Each Approach

**Use polling when:**
- The system is simple and dedicated to a single task
- Predictable timing is more important than efficiency
- The events occur frequently and regularly
- You need to avoid the complexity of interrupt handling

**Use interrupts when:**
- The system needs to perform multiple tasks efficiently
- Events are infrequent or unpredictable
- Quick response time to events is critical
- CPU resources need to be conserved
- The main program needs to do substantial work between events

Both methods are valid design choices depending on the application requirements, system constraints, and complexity tolerance.
