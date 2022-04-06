# SIC-XE_Assembler

## Foreward  

經過一個暑假從Coursera學簡單的Python課程，第一次使用Python寫比較大的程式，小試身手。  
如有寫不好的地方，還請見諒。

## Lexical Analysis  

### Introduction  

1. 程式的功能要正確的切出每一個Token。
2. 並且將每一個Token對應到正確的Table裡的位置。  
3. Table1~4會是保留字。  
4. Table5~7必須要使用Hash Function來做放入，遇到碰撞便往下一個位置。  

### Files  

1. token.py 為完整程式碼
2. SIC_input.txt 為測試檔案
3. output.txt 為輸出檔案

## Cross Assembler

1. 主要的目的是將程式碼翻譯成機器碼（Object Code）。  
2. 計算每一行指令的所在位置。  
3. 同時也會做文法上的檢測（Syntax Analysis），檢測出程式碼的錯誤。  
4. 最後將結果輸出在螢幕中和寫入檔案中。  
