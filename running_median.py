import streamlit as st
import heapq
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Initialize session state for heaps and number list
if 'min_heap' not in st.session_state:
    st.session_state.min_heap = []  # Min-heap for the larger half
if 'max_heap' not in st.session_state:
    st.session_state.max_heap = []  # Max-heap (inverted min-heap) for the smaller half
if 'numbers' not in st.session_state:
    st.session_state.numbers = []

st.set_page_config(page_title="Running Median with Heaps", layout="centered")
st.title("📊 Running Median Finder Using Heaps")
st.markdown("""
This app demonstrates how to maintain a **running median** using two heaps:
- A **max heap** for the smaller half of the data
- A **min heap** for the larger half of the data
""")

number = st.number_input("Enter a number to insert:", step=1, format="%d")
if st.button("Insert Number"):
    st.session_state.numbers.append(number)

    # Insert into the appropriate heap
    if not st.session_state.max_heap or number <= -st.session_state.max_heap[0]:
        heapq.heappush(st.session_state.max_heap, -number)
    else:
        heapq.heappush(st.session_state.min_heap, number)

    # Balance the heaps
    if len(st.session_state.max_heap) > len(st.session_state.min_heap) + 1:
        moved = -heapq.heappop(st.session_state.max_heap)
        heapq.heappush(st.session_state.min_heap, moved)
    elif len(st.session_state.min_heap) > len(st.session_state.max_heap):
        moved = heapq.heappop(st.session_state.min_heap)
        heapq.heappush(st.session_state.max_heap, -moved)

    st.success(f"Inserted {number}!")

# Display entered numbers
st.subheader("🔢 Numbers Entered")
st.write(", ".join(map(str, st.session_state.numbers)) if st.session_state.numbers else "None")

# Calculate and show median
if st.session_state.numbers:
    if len(st.session_state.max_heap) == len(st.session_state.min_heap):
        median = (-st.session_state.max_heap[0] + st.session_state.min_heap[0]) / 2
    else:
        median = -st.session_state.max_heap[0]

    st.markdown("""
    <div style='background-color:#ffd700; padding:20px; border-radius:10px; text-align:center;'>
        <h2 style='color:#000;'>📍 <u>Current Median</u></h2>
        <h1 style='color:#d63384;'>💡 {:.2f}</h1>
    </div>
    """.format(median), unsafe_allow_html=True)

    # Visualization of heaps as circles
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 2)
    ax.axis('off')

    # Draw Max Heap (left side)
    ax.text(1, 1.5, 'Max Heap', fontsize=12, weight='bold')
    max_vals = sorted([-x for x in st.session_state.max_heap], reverse=True)
    if len(max_vals) > 2:
        circle = Circle((2.5, 1), 1.0, color='#1f77b4', alpha=0.8)
        ax.add_patch(circle)
        text = ", ".join(map(str, max_vals))
        ax.text(2.5, 1, text, color='white', ha='center', va='center', fontsize=9, wrap=True)
    else:
        for i, val in enumerate(max_vals):
            x = 1 + i * 1.2
            circle = Circle((x, 1), 0.5, color='#1f77b4', alpha=0.8)
            ax.add_patch(circle)
            ax.text(x, 1, str(val), color='white', ha='center', va='center', fontsize=10)

    # Draw Min Heap (right side)
    ax.text(7, 1.5, 'Min Heap', fontsize=12, weight='bold')
    min_vals = sorted(st.session_state.min_heap)
    if len(min_vals) > 2:
        circle = Circle((8.5, 1), 1.0, color='#ff7f0e', alpha=0.8)
        ax.add_patch(circle)
        text = ", ".join(map(str, min_vals))
        ax.text(8.5, 1, text, color='white', ha='center', va='center', fontsize=9, wrap=True)
    else:
        for i, val in enumerate(min_vals):
            x = 7 + i * 1.2
            circle = Circle((x, 1), 0.5, color='#ff7f0e', alpha=0.8)
            ax.add_patch(circle)
            ax.text(x, 1, str(val), color='white', ha='center', va='center', fontsize=10)

    st.pyplot(fig)

# Reset button
if st.button("Reset"):
    st.session_state.numbers.clear()
    st.session_state.max_heap.clear()
    st.session_state.min_heap.clear()
    st.info("State has been reset.")