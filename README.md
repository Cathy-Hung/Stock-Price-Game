## (1) 程式的功能 Features
此程式是一個簡易版的股票交易遊戲，模擬股票市場的價格波動，讓玩家體驗股票交易的過程。

## (2) 使用方式 Usage
按下 Start 開始遊戲後，股票價格將隨機波動。玩家可以根據股價波動決定是否買入或賣出股票，分別按下 BUY STOCK 或 SALE STOCK 進行交易。此外，玩家還可以透過右下方的滑桿選擇向銀行借款的金額。
在進行最後金額計算時，須先以本金加利息還清債務，還清後剩餘的現金將獲得利息，同時發放現金股利並以當時股價將剩餘股票轉換成現金，故玩家應充分考慮股價、股息及利息等因素以在遊戲結束時得到最高的金額。

## (3) 程式的架構 Program Architecture
### 1. 遊戲解說介面
設定初始值/遊戲規則文字/start按鈕的新增
### 2. 遊戲進行介面
版面配置/股價的設定及動態折線圖的繪製/購買售出股票的程序/玩家資料的即時顯示/貸款程序
### 3. 遊戲結束介面
最終金額的計算與呈現/Exit按鈕的新增

## (4) 開發過程 Development Process
1. 由於對 tkinter 的寫法不熟悉，我首先將遊戲解說頁面的需求寫給 ChatGPT，直接使用其設計的程式作為基礎，然後加入自己撰寫的遊戲規則，並對顏色、字體和版面配置進行了微調。隨後，我再求助 ChatGPT 設計切換頁面的功能。

2. 接著，我使用 matplotlib.pyplot 撰寫了一段用於繪製股價即時動態波動折線圖的程式碼:
```import random
import matplotlib.pyplot as plt

def plot_update(ax, times, prices):
    ax.clear()  
    plt.xlim(0, 300)
    plt.ylim(43, 58)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Stock Price')
    ax.set_title('Stock Price Over Time')
    ax.plot(times, prices, color='#9a4741', linewidth=2)
    ax.scatter(times, prices, color='#9a4741',s=5)
    ax.text(0.05, 1.02, f'Time: {times[-1]:.1f} sec\nPrice: {prices[-1]:.2f}', transform=ax.transAxes)
    plt.pause(1)  

plt.figure()
ax = plt.gca()  

total_time = 300  
times, prices = [], []  
current_price = random.uniform(45, 55)
times.append(0)
prices.append(current_price)
for t in range(1, total_time + 1):
    current_price += random.uniform(-0.5, 0.5)  
    current_price = max(45, min(55, current_price))  
    times.append(t)
    prices.append(current_price)
    plot_update(ax, times, prices)
plt.show()```
，然後將其提供給 ChatGPT，請其協助改寫成可以匯入到 tkinter 遊戲介面中的版本。

3. 隨後，我自行撰寫了處理玩家購買股票並即時更新資產資訊的程式碼，並在 ChatGPT 的輔助下修改，使其能即時變動數據，且加入了錯誤提示的彈跳視窗功能。同時，我以購買股票的程式碼改寫售出股票的程式碼。

4. 最後，我再次利用 ChatGPT 的協助，設定遊戲秒數倒數結束後自動切換到遊戲結束頁面，並改寫先前的程式，新增頁面上需要顯示的文字內容。接著，我設計了計算玩家最終金額的邏輯，並改寫先前程式將計算結果呈現在結束頁面上及新增退出按鈕。

## (5) 參考資料來源 References
1. [Moblab]https://www.moblab.com/edu/games/asset-market-bubbles-and-crashes
2. [Chatgpt]

## (6) 程式修改或增強的內容 Enhancements and Contributions
遊戲的發想參考自Moblab的資產市場遊戲。原本是一個互動式的遊戲，股票的買家和賣家共同決定交易價格。經過修改後，遊戲被設計為單人遊玩，並且股票價格的波動性更加貼近現實市場，呈現連續的波動模式。同時，我還加入了借款功能，並利用拉桿裝置來調整借款金額。後續的程式設計由ChatGPT提供協助。