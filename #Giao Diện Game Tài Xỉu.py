#Giao Diện Game Tài Xỉu
#Code by Huy Bảo
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
#Lớp đối tượng các tính năng trong game 
class GameTaiXiuGUI:
    def __init__(self, master):
        #Phuơng thức các hàm
        self.tien_con_lai = 0
        self.tien_nap_ban_dau = 0
        self.i = 0
        #Tạo các label hiện lên cho người chơi vào
        #Label số dư
        self.label_tien = tk.Label(master, text="Số dư: $0")
        self.label_tien.pack()
        #Label nạp tiền
        self.button_nap_tien = tk.Button(master, text="Nạp tiền", command=self.nap_tien)
        self.button_nap_tien.pack()
        #Label bắt đầu game 
        self.button_choi = tk.Button(master, text="Bắt đầu chơi", command=self.bat_dau_choi, state=tk.DISABLED)
        self.button_choi.pack()
    #Hàm nạp tiền 
    def nap_tien(self):
        try:
            t = simpledialog.askstring("Nạp tiền", "Nhập số dư muốn nạp ($): ")
            if t.lower() == "all":
                t = self.tien_nap_ban_dau
            else:
                t = int(t)
                if 0 < t <= 1000000:
                    self.tien_con_lai = t
                    self.tien_nap_ban_dau = t
                    self.update_label_tien()
                    self.button_choi.config(state=tk.NORMAL) # Khi đã nạp tiền, cho phép chơi
                else:
                    messagebox.showinfo("Vượt quá giới hạn. Tối đa $1000000")
        except ValueError:
            messagebox.showinfo("Vui lòng nhập số. Không nhập chữ")
    #Hàm update tiền 
    def update_label_tien(self):
        self.label_tien.config(text=f"Số dư: ${self.tien_con_lai}")
    # Phương thức bắt đầu chơi
    def bat_dau_choi(self):
        them_tien = ""
        if self.tien_con_lai == 0:
            them_tien = simpledialog.askstring("Hết tiền", "Số dư của bạn đã hết. Bạn muốn nạp thêm tiền không? (y/n): ")
            if them_tien.lower() == "n":
                print("Chúc bạn một ngày tốt lành!")
                self.master.destroy()
                return
            elif them_tien.lower() == "y":
                self.tien_con_lai = self.nhaptien()
                self.update_label_tien()
        self.i += 1
        td = simpledialog.askstring("Số dư cược", "Nhập số dư muốn cược ($): ")
        if td.lower() == "all":
            td = self.tien_con_lai
        else:
            td = int(td)
        if td > self.tien_con_lai:
            messagebox.showinfo("Thông báo", "Số tiền đặt cược vượt quá số dư")
            return
        v = simpledialog.askstring("Chọn TÀI hoặc XỈU", "Mời bạn chọn TÀI hoặc XỈU (t/x): ")
        a, b, c, tong = self.taixiu()
        # Gọi phương thức in_xuc_xac
        self.in_xuc_xac(a, b, c, tong)
        kq_tai_xiu = "TÀI" if tong >= 11 else "XỈU"
        messagebox.showinfo("Kết quả", f"Xúc xắc 1: {a}\nXúc xắc 2: {b}\nXúc xắc 3: {c}\nTổng: {tong}\nKết quả: {kq_tai_xiu}")
        if v == kq_tai_xiu:
            self.tien_con_lai = self.thang_cuoc(td)
        else:
            self.tien_con_lai = self.thua_cuoc(td)
        self.update_label_tien()
        self.master.after(1000, self.bat_dau_choi)#Hết AI
    #Hàm ra kết quả
    def taixiu(self):
        xucxac = self.custom_xucxac()
        random.seed(xucxac)
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        tong = a + b + c
        return a, b, c, tong
    #Hàm in xúc xắc
    def in_xuc_xac(self, a, b, c, tong):
        time.sleep(2)
        print("\n>>> Xúc xắc 1 ra", a, "nút")
        time.sleep(2)
        print(">>> Xúc xắc 2 ra", b, "nút")
        time.sleep(2)
        print(">>> Xúc xắc 3 ra", c, "nút")
        time.sleep(1)
        print(">>> Tổng là", tong, "nút\n")    
    #Hàm custom kết quả xúc xắc 
    #xx = thgian hiện tại*thgian hiện tại*1000
    def custom_xucxac(self):
        return int(time.time() * time.time() * 1000)
    #Hàm nếu thắng cược
    def thang_cuoc(self, td):
        win_amount = td * 2
        self.tien_nap_ban_dau += win_amount
        self.tien_con_lai = self.tien_nap_ban_dau
        print(f"=> Bạn đã thắng ${win_amount}\n=> Tổng số dư còn lại: ${self.tien_con_lai}\n")
        return self.tien_con_lai
    #Hàm nếu thua cược
    def thua_cuoc(self, td):
        self.tien_nap_ban_dau -= td
        self.tien_con_lai = self.tien_nap_ban_dau
        print(f"=> Bạn đã thua ${td}\n=> Tổng số dư còn lại: ${self.tien_con_lai}\n")
        return self.tien_con_lai
    #Hàm nhập tiền
    def nhaptien(self):
        try:
            t = int(simpledialog.askstring("Nạp tiền", "Nhập số dư muốn nạp ($): "))
            if 1 <= t <= 1000000:
                return t
        except ValueError:
            pass  # Xử lý nếu người dùng nhập không đúng
    #Hàm tiếp tục chơi
def choitiep(tien_con_lai, nhaptien, update_label_tien):
    while True:
        tiep_tuc = input("Bạn có muốn chơi tiếp không? (y/n): ")
        if tiep_tuc.lower() == "y":
            break
        elif tiep_tuc.lower() == "n":
            print(f"Cảm ơn bạn đã chơi. Số dư còn lại: ${tien_con_lai}")
            print("Chúc bạn một ngày tốt lành!")
            exit(0)
        else:
            print("Vui lòng nhập đúng.")
#Hàm chính chạy chương trình
def main():
    root = tk.Tk()
    game_tai_xiu_gui = GameTaiXiuGUI(root)
    root.mainloop()
    # Sau khi game kết thúc lần đầu, chương trình sẽ được thực hiện cho chạy tiếp. 
    choitiep(game_tai_xiu_gui.tien_con_lai, game_tai_xiu_gui.nhaptien, game_tai_xiu_gui.update_label_tien)
main()