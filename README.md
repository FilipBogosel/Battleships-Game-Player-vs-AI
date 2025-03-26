# 🚢 Naval Clash: Python Battleship

**Command the seas in this terminal-based strategy classic!**  
Outsmart a cunning AI opponent in a battle of wits and precision.

---

## 🌟 Key Features

- **Strategic Warfare**  
  Place 5 ships (2-4 units long) using smart positioning
- **Intel System**  
  Track hits (🔥) and misses (🌊) on both boards
- **Adaptive AI**  
  Computer opponent learns from your patterns
- **Clean UI**  
  ASCII-based boards with real-time updates
- **Instant Feedback**  
  Color-coded attack results and victory detection

---

## ⚡ Quick Start

```bash
git clone https://github.com/your-repo/python-battleship.git
cd python-battleship
pip install texttable
python start.py
```
# Board Demo
```
Your Board            Computer's Board
+---+---+---+        +---+---+---+
| S | S | ~ |        | ~ | ~ | ~ |
| X | 🌊 | ~ |        | 🌊 | ~ | ~ |
| ~ | ~ | ~ |        | ~ | ~ | 🔥 |
+---+---+---+        +---+---+---+
```
# Playing sample
Enter your shot coordinates (x y): 2 2
💥 Direct hit! Computer's ship damaged!

Computer attacks (3,4)
🌊 Miss! Their shot lands in water...

# 🛠️ Dev Features
100% Test Coverage
Battle-tested logic with 25+ unit tests

Smart AI
Focused attack patterns after successful hits

Error Handling
Invalid moves blocked with clear feedback

Modular Design
Easy to modify ship configurations/rules

