import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# 模擬遊戲玩家狀態
player_cash = 200  
player_stock = 2  
player_loan = 0  

def main():
    global root
    # 創建主窗口
    root = tk.Tk()
    root.title("Irrational Exuberance: Stock Trading Game")
    root.geometry("1200x800")  # 設置窗口大小
    root.configure(bg="white")  # 設置純白背景顏色

    # 添加標題
    title_label = tk.Label(
        root,
        text="Irrational Exuberance: Stock Trading Game",
        font=("Verdana", 28, "bold"), 
        fg="black",
        bg="white",
        pady=20,
    )
    title_label.pack()

    # 添加遊戲規則說明
    rules = (
        "Game rules: \n"
        "1. At the beginning of the game, players are allocated 200 cash and two shares of stock.\n"
        "2. The game time is three minutes, and the stock price will fluctuate over time. \n"
        "3. There are two possible dividends, randomly generated and will be distributed to the\n"
        "   player at the end of the game.\n"
        "4. Players can decide to buy or sell stocks based on the real-time stock price displayed \n"
        "   in the upper left corner.  \n"
        "5. When you have insufficient cash, you can use the lever in the lower right corner to \n"
        "   select the loan amount. \n"
        "6. At the end of the game, the loan will be repaid with principal and interest. \n"
        "7. The remaining cash will receive the same amount of interest, and the remaining stocks\n"
        "   will be converted into cash based on the current stock price, dividends will be\n"
        "   issused, and the final amount will be calculated."
    )
    rules_label = tk.Label(
        root,
        text=rules,
        font=("Verdana", 16), 
        justify="left",
        fg="black",
        bg="white",
        padx=200,
        pady=10,
    )
    rules_label.pack(anchor="center")

    # 添加 Start 按鈕
    start_button = tk.Button(
        root,
        text="Start!",
        font=("Times New Roman", 18, "bold"),  
        bg="#75828b",  
        fg="white",
        activebackground="#323f52",  
        activeforeground="white",
        command=start_game,
    )
    start_button.pack(pady=20)  # 使用 pack 布局

    # 啟動主循環
    root.mainloop()

def start_game():
    open_main_game_window()  # 切換到主遊戲介面

def open_main_game_window():
    """切換到主遊戲介面"""
    for widget in root.winfo_children():
        widget.destroy()  # 清空當前所有組件

    # 創建主框架
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 左側框架（包含圖形）
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    # 右側框架（包含現金和股票信息）
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

    # 創建 matplotlib 圖形並設置大小 (400x600)
    fig, ax = plt.subplots(figsize=(6, 4)) 

    # 用來存儲最新的股價
    global nowprice
    nowprice = 0  # 初始股價

    def plot_update(ax, times, prices):
        ax.clear()  
        ax.set_xlim(0, 180)  # 設置 x 軸範圍
        ax.set_ylim(43, 58)  # 設置 y 軸範圍
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Stock Price')
        ax.set_title('Stock Price Over Time')

        # 繪製股價折線和散點圖
        ax.plot(times, prices, color='#9a4741', linewidth=2)
        ax.scatter(times, prices, color='#9a4741', s=5)

        # 顯示當前時間和股價
        ax.text(0.05, 1.02, f'Time: {times[-1]:.1f} sec\nPrice: {prices[-1]:.2f}', transform=ax.transAxes)
        
        global nowprice
        nowprice = prices[-1]  

        # 更新畫布
        canvas.draw()

    # 將圖形嵌入 tkinter 窗口並放置於左側框架
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.get_tk_widget().pack(pady=20)

    # 模擬參數
    total_time = 180  # 300 秒
    times, prices = [], []  # 時間和股價的列表

    # 初始化隨機股價
    current_price = random.uniform(45, 55)
    times.append(0)
    prices.append(current_price)

    # 開始模擬股價波動並更新圖形
    def update(t=1):
        nonlocal current_price  # 使用外部變量 current_price

        if t <= total_time:
            # 股價隨機波動
            current_price += random.uniform(-0.5, 0.5)  # 每秒股價上下波動 0.5
            current_price = max(45, min(55, current_price))  # 限制股價在 45 到 55 之間

            # 添加時間和股價到列表
            times.append(t)
            prices.append(current_price)

            # 更新圖形
            plot_update(ax, times, prices)

            # 每 1000 毫秒後更新一次，模擬每秒股價變動
            root.after(1000, update, t+1)  # 1000 毫秒（即 1 秒）後再調用一次 update 函數
        else:
            final_page() 

    # 直接開始運行模擬
    update()

    def buy_stock():
        global player_cash, player_stock
        if player_cash >= nowprice:  
            player_cash -= nowprice  
            player_stock += 1  
            update_player_info()  
        else:
            messagebox.showerror("Error", "Not enough cash to buy stock!")


    def sale_stock():
        global player_cash, player_stock
        if player_stock > 0:  
            player_cash += nowprice  
            player_stock -= 1  
            update_player_info() 
        else:
            messagebox.showerror("Error", "No stock to sell!")


    buy_button = tk.Button(
        left_frame,
        text="BUY STOCK",
        font=("Times New Roman", 18, "bold"),  
        bg="#75828b",  
        fg="white",
        activebackground="#323f52",  
        activeforeground="white",
        command=buy_stock,
    )
    buy_button.pack(pady=20)  


    sale_button = tk.Button(
        left_frame,
        text="SELL STOCK",
        font=("Times New Roman", 18, "bold"),  
        bg="#75828b",  
        fg="white",
        activebackground="#323f52",  
        activeforeground="white",
        command=sale_stock,
    )
    sale_button.pack(pady=20)  

    # 顯示玩家資料
    player_info_label = tk.Label(
        right_frame,
        text=f"Cash: ${player_cash:.2f}\nStocks: {player_stock} shares\nLoan: ${player_loan:.2f}\nInterest Rate: 4%\nDividend: $1.00/6.00",
        font=("Times New Roman", 18),
        bg="white",
        fg="black",
    )
    player_info_label.pack(pady=20)

    # 更新玩家資料的函数
    def update_player_info():
        player_info_label.config(text=f"Cash: ${player_cash:.2f}\nStocks: {player_stock} shares\nLoan: ${player_loan:.2f}\nInterest Rate: 4%\nDividend: $1.00/6.00")


    def borrow_money():
        global player_cash, player_loan
        borrowed_amount = borrow_slider.get()
        player_cash += borrowed_amount  
        player_loan += borrowed_amount  
        update_player_info()  

    borrow_label = tk.Label(
        right_frame,
        text="Borrow Money From Bank ($0-$50)",
        font=("Times New Roman", 16),
        bg="white",
        fg="black",
    )
    borrow_label.pack(pady=10)

    borrow_slider = tk.Scale(
        right_frame,
        from_=0,
        to=50,
        orient="horizontal",
        length=300,
        font=("Times New Roman", 14),
    )
    borrow_slider.pack(pady=10)

    # 顯示借款金額
    borrow_amount_label = tk.Label(
        right_frame,
        text="Amount: $0",
        font=("Times New Roman", 16),
        bg="white",
        fg="black",
    )
    borrow_amount_label.pack(pady=10)

    def update_borrow_amount_label(event):
        borrow_amount_label.config(text=f"Amount: ${borrow_slider.get()}")

    borrow_slider.bind("<Motion>", update_borrow_amount_label)
    borrow_button = tk.Button(
        right_frame,
        text="BORROW",
        font=("Times New Roman", 18, "bold"),  
        bg="#75828b",  
        fg="white",
        activebackground="#323f52",  
        activeforeground="white",
        command=borrow_money,
    )
    borrow_button.pack(pady=20)

def final_page():
    global nowprice
    for widget in root.winfo_children():
        widget.destroy()  

    summary_label = tk.Label(
        root,
        text="Game Over! Here is your result:",
        font=("Verdana", 24, "bold"),
        fg="black",
        bg="white",
        pady=20
    )
    summary_label.pack()
    interest_rate=1.04
    dividend=random.choice([1, 5])
    total_cash=(player_cash - player_loan * interest_rate)*interest_rate + (player_stock * nowprice) + (player_stock * dividend)

    # 顯示玩家最終數據
    final_info = f"Final Amount: ${total_cash:.2f}"
    final_data_label = tk.Label(
        root,
        text=final_info,
        font=("Verdana", 16),
        fg="black",
        bg="white",
        pady=10
    )
    final_data_label.pack()

    exit_button = tk.Button(
        root,
        text="Exit",
        font=("Times New Roman", 18, "bold"),  
        bg="#75828b",  
        fg="white",
        activebackground="#323f52",  
        activeforeground="white",
        command=root.destroy
    )
    exit_button.pack(pady=20)

if __name__ == "__main__":
    main()
