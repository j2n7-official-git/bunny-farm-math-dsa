"""
Chào mừng bé đến với trò chơi Nông Trại Thỏ Ngọc và Cuộc Chiến Số Học Nhí Đồng!
Trong trò chơi này bé sẽ vào vai Chú Nông Chuyên Nghiệp dùng trí tuệ để cứu vườn.
Các con số từ âm đến dương sẽ biến thành số củ cà rốt hoặc số sâu bọ gây hại.
Trước tiên cấu trúc Hàng Đợi Queue được dùng để quản lý các bạn thỏ xếp hàng.
Tiếp theo cấu trúc Ngăn Xếp Stack là túi phép thuật giúp bé rút lại nước đi sai.
Cây Tìm Kiếm Nhị Phân BST dùng để sắp xếp kho hạt giống theo thứ tự tăng dần.
Thuật toán Cửa Sổ Trượt Rolling Window giúp bé tìm 3 ngày thu hoạch nhiều nhất.
Bé sẽ phải tính toán tổng năng lượng và giải các câu đố số học để vượt qua.
Trò chơi giúp các bé cấp 1 luyện phản xạ tính nhẩm và làm quen với thuật toán.
Mỗi lượt chơi bé được chọn xử lý hàng đợi, hoàn tác hoặc xem kho hạt giống BST.
Nếu tính đúng tổng cửa sổ trượt bé sẽ nhận được hạt giống và cộng điểm thưởng.
Nếu tính sai thỏ sẽ bị giảm năng lượng HP do sâu bọ tấn công vào khu vườn.
Các mã lệnh được viết bằng Python 3 rất dễ hiểu kèm theo chú thích chi tiết.
Chúc các bé có những giờ phút vừa học vừa chơi thật vui và thành nhà toán học!
Cùng bắt đầu hành trình khám phá thế giới số học kỳ diệu ngay bây giờ nhé!
"""
import random #Thư viện tạo số ngẫu nhiên để tạo thử thách cho bé

# === 1. Cấu trúc dữ liệu cây BST (KHO HẠT GIỐNG) ===
class NodeBST:
    """
    1. Khởi tạo một nút chứa hạt giống trong cây nhị phân
    2. Mỗi hạt giống gô một con số (key) và tên vật phấn
    3. Hai nhánh left và  right dùng để liên kết các hạt giống (seed) khác
    """
    def __init__(self, key, name):
        self.key = key #Lưu số định danh của hạt giống (-2026 đến 2027)
        self.name = name #Lưu tên hiển thị của hạt giống
        self.left = None #Nhánh bên trái ban đầu chưa trỏ đi đâu
        self.right = None #Nhánh bên phải ban đầu chưa trỏ đi đâu

class BunnyBST:
    """
    1. Quản lí khko hạt giống bằng Cây Tìm Kiếm Nhị Phân
    2. Hạt giống ố nhỏ hơn nằm bên trái, lớn hơn nằm bên phải
    3. Giúp bé in ra kho đồ đã sắp xếp tự động từ nhỏ đến ớn
    """
    def __init__(self):
        self.root = None #Gốc cây ban đầu chưa có hạt giống nào

    def insert(self, key, name):
        """
        1. Thêm hạt giống mới vào vị trí thích hợp trên cây
        2. So sánh giá trị để tìm vị trí trống ở nhánh trái hoặc phải
        4. Giữ cho kho hạt giống luôn ngăn nắp theo thứ tự
        """
        if not self.root: #Nếu cây chưa c gốc
            self.root = NodeBST(key, name) #Tạo hạt giống đầu tiên làm gốc
            return #Kết thúc hàm
        curr = self.root #Bắt đầu duyệt từ gốc cây
        while True: #Vòng lặp tìm vị trí chèn
            if key < curr.key:  # Nếu số mới nhỏ hơn số hiện tại
                if not curr.left: #Nếu nhánh trái đang trống
                    curr.left = NodeBST(key, name) #Gắn hạt giống vào trái
                    break # Dừng vòng lặp
                curr = curr.left #Tới nút tiếp theo bên trái
            else: #Nếu số mới lớn hơn hoặc bằng
                if not curr.right: #Nếu nhánh phải đang trống
                    curr.right = NodeBST(key, name) #Gắn hạt giống vào phải
                    break #Dừng vòng lặp
                curr = curr.right #Tới nút tiếp theo bên phải

    def inorder(self, node, res):
        """
        1. Duyệt cây theo thứ tự Trung Thứ (Left - Node - Right)
        2. Thu thập hạt giống theo thứ tự giá trị
        3. Trả kết quả vào danh sách res để hiện thị ra màn hình
        """
        if node: #Nếu nút hiện tại có dữ liệu
            self.inorder(node.left, res) #Duyệt hết nhánh bên trái
            res.append((node.key, node.name)) #Thêm hạt giống vào danh sách
            self.inorder(node.right, res) #Duyệt tiếp nhánh bên phải

# === 2. CẤU TRÚC STACK (TÚI HOÀN TÁC) & QUEUE (HÀNG ĐỢI) ===
class UndoStack:
    """
    1. Ngăn xếp Stack giúp bé rút lại nước đi vừa thực hiện
    2. Hoat động theo quy tắc LIFO (Last-In, First-Out): Vào sau cùng thì ra đầu tiên
    3. Bảo vệ HP và điểm số khi bé bấm nhầm lệnh
    """
    def __init__(self):
        self.items = [] #Tạo danh sách rỗng làm ngăn xếp

    def push(self, state):
        self.items.append(state) #Thêm trạng thái game vào đỉnh stack

    def pop(self):
        if len(self.items) > 0: #Nếu stack có dữ liệu
            return self.items.pop() #Lấy trạng thái gần nhất ra
        return None #Trả về None nếu stack rỗng

class AnimalQueue:
    """
    1. Hàng đợi Queue quản lý các bạn Thỏ đang xếp hàng xin giúp
    2. Hoạt động theo quy tắc FIFO (First-In First-Out): Bạn nào đến trước được giúp trước\
    3. Đảm bảo thử thách diễn ra đúng thứ tự xếp hàng
    """
    def __init__(self):
        self.queue = [] #Tạo danh sách rỗng làm hàng đợi

    def enqueue(self, animal):
        self.queue.append(animal)

    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

# === 3. THUẬT TOÁN CỬA SỔ TRƯỢT (ROLLING WINDOW / SLIDING WINDOW) ===
def find_best_3days(days):
    """
    1. Tìm tổng 3 ngày liên tiếp có thu hoạch ớn nhất
    2. Cộng 3 ngày đầu rồi trượt cửa sổ qua các ngày tiếp theo
    3. Trả về ết quả tổng chính xác để đối chiếu với bé
    """
    max_sum = sum(days[:3]) #Tiính tổng 3 ngày đầu tiên
    curr_sum = max_sum #Đặt tổng hện tại bằng tổng đầu tiên
    for i in range(len(days) - 3):
        curr_sum = (curr_sum - days[i] + days[i + 3]) #Bớt ngày cũ, thêm ngày mới
        if curr_sum > max_sum: #Nếu tổng mới lớn hơn
            max_sum = curr_sum #Cập nhật tổng lớn nhất
    return max_sum # Trả về đáp án đúngd

# === 4. MAIN GAME - BUNNY GAME ENGINE ===
class BunnyGame:
    """
    1. Quan lý toàn bộ luồng chơi của Nông Trại Thỏ Ngọc
    2. Kết hợp cả 4 cấu trúc dữ liệu trong từng lượt chơi
    3. Tạo môi trường đấu trí số học nhẹ nhaàng và vui vẻ cho bé
    """
    def __init__(self):
        self.hp = 120 # Điểm năng lượng ban đầu của Thỏ là 120
        self.score = 0 # Điểm số ban đầu của bé là 0
        self.stack = UndoStack() # Tạo túi hoàn tác Stack
        self.queue = AnimalQueue() #T ạo hàng đợi Thỏ Queue
        self.bst = BunnyBST() # Tạo kho hạt giống BST
        self.generate_animals() #T ạo danh sách các bạn Thỏ ban đầu
        
    def generate_animals(self):
        """
        1. Tạo ngẫu nhiên 3 bạn Thỏ cuàng mảng số thu hoạch 5 ngày
        2. - Số dương đại diện cho: CÀ RỐT
           - Số âm đại diện cho: SÂU BỌ
        3. Đưa các bạn Thỏ vào Hàng đợi Queue để chờ bé giúp
        """
        for i in range(3):
            days = [
                random.randint(-15, 30) for _ in range(5)
            ] #5 số từ -15 đến 30
            self.queue.enqueue((f"Thỏ Bông #{i+1}", days)) #Đưa vào queue

    def play(self):
        """
        1. Hiển thị giao diện menu và xử lý lượt chọn của bé
        2. Kiểm tra kết quả tính nhẩm tổng 3 ngày thu hoạch
        3. Cập nhật HP, Score và hạt giống (seed) vào BST khi bé thắng
        """
        #Tiêu đề
        print("==============================================================")
        print("||         NÔNG TRẠI THỎ NGỌC - GAME ĐẤU TRÍ SỐ HỌC         ||")
        print("==============================================================")
        print(f"Năng lượng (HP): {self.hp} | Điểm số: {self.score}") #Trạng thái
        print("1. Giúp thỏ thu hoạch (Test: QUEUE + SLIDING WINDOWS)") #Option 1
        print("2. Rút lại nước sai (Stack Undo)") #Option 2
        print("3. Xem Kho Hạt Giống (BST Inorder)") #Option 3
        print("4. Hướng dẫn chơi (Cẩm năng nông dân)") #New option: Game manual instruction
        print("5. Thoát game") #Option 5

        choice = input("Bé chọn chức năng (1-5): ").strip() #Nhận lựa chọn
        if choice == "1": #Nếu bé chọn giải đố
            animal = self.queue.dequeue() #Ly thỏ ở đầu hàng đợi
            if not animal: #Nếu hàng đợi đã hết thỏ
                print("Đã hết Thỏ xếp hàng! Đang mời thêm các bạn Thỏ...")
                self.generate_animals() #Tạo thêm thỏ mới
                return # Quay lại lượt sau
            self.stack.push((self.hp, self.score)) # Lưu lại HP và Score vào Stack
            name, days = animal #Lấy tên thỏ và mảng 5 ngày
            print(f"\n Bạn {name} mang đến chuỗi 5 ngày thu hoạch: {days}")
            print("(Số dương = Cà rốt tươi, Số âm = Sâu bọ cắn)")
            correct_ans = find_best_3days(days) #Thuật toán tính đáp án
            try:
                ans = int(
                    input("Đố bé: Tổng 3 ngày liên tiếp tốt nhất là bao nhiêu? ")
                )
                if ans == correct_ans: #Bé tính đúng
                    print(" CHÚC MỪNG! Bé đã tính đúng và cứu được khu vườn! ")
                    self.score += 20 #Thường 20 điểm
                    seed_val = random.randint(-120, 120) #Tạo hạt giống mới
                    self.bst.insert(
                        seed_val, f"Hạt Giống Cà Rốt Sức Mạnh [{seed_val}]"
                    ) #Lưu BST
                else: #Nếu bé tính sai
                    print(
                        f"Sai mất rồi! Đáp án đúng là {correct_ans}. Thỏ bị trừ 10HP!"
                    )
                    self.hp -= 10 #Phạt trừ 10HP
            except ValueError: #Bé nhập chữ thay vì số
                print("Bé hãy nhập số nguyên nhé!")

        elif choice == "2": #Bé chọn hoàn tác
            prev = self.stack.pop() #Rút trạng thái cũ từ Stack
            if prev:              #Nếu có trạng thái cũ
                self.hp, self.score = prev #Khôi phục HP và Score
                print("Đã rút lại nước đi thành công!")
            else:                 #STACK empty
                print("Chưa có nước đi nào để rút lại!")

        elif choice == "3":     #Bé chọn xem kho BST
            res = [] #Danh sách tạm
            self.bst.inorder(self.bst.root, res) #Duyệt BST\
            print("\n--- KHO HẠT GIỐNG CÂY THEO SẮP XẾP TĂNG DẦN ---")
            if not res:
                print("(Kho hạt giống đang trống)")
            for key, item in res:
                print(f"Giá trị hạt: {key:3d} -> {item}") #In danh sách hạt giống


        elif choice == "4":  # HƯỚNG DẪN CHƠI (16 DÒNG PRINT - NHÓM THÀNH 4 ĐOẠN)
            print("\n===============================================================")
            print("||             CẨM NANG HƯỚNG DẪN NÔNG TRẠI THỎ NGỌC         ||")
            print("===============================================================")
            # --- ĐOẠN 1: BỐI CẢNH & KHÁI NIỆM SỐ HỌC (4 DÒNG) ---
            print("[1. CỐT TRUYỆN & Ý NGHĨA CÁC CON SỐ]")
            print("   - Cà rốt & Sâu bọ: Số DƯƠNG là củ Cà Rốt ngọt, số ÂM là Sâu Bọ phá hoại.")
            print("   - Hàng đợi trợ giúp: Các bạn Thỏ sẽ xếp hàng lần lượt chờ bé giải cứu.")
            print("   - Thứ tự xếp hàng: Bạn Thỏ nào đến trước sẽ được bé trợ giúp trước.")
            # --- ĐOẠN 2: THỬ THÁCH TÍNH NHẨM (4 DÒNG) ---
            print("\n[2. THỬ THÁCH CỬA SỔ NĂNG LƯỢNG]")
            print("   - Nhiệm vụ: Tìm ra 3 ngày liên tiếp có tổng năng lượng lớn nhất.")
            print("   - Mẹo tính nhẩm: Tính tổng 3 ngày đầu, rồi trượt dần sang các ngày tiếp theo.")
            print("   - Phần thưởng & Hình phạt: Tính ĐÚNG nhận điểm + Hạt giống, SAI sẽ bị mất HP.")
            # --- ĐOẠN 3: CÁC CÔNG CỤ HỖ TRỢ (4 DÒNG) ---
            print("\n[3. TÚI PHÉP THUẬT & KHO BÁU]")
            print("   - Túi Hoàn Tác (Chức năng 2): Rút lại lượt chơi trước nếu lỡ tính nhầm.")
            print("   - Kho Hạt Giống (Chức năng 3): Nơi cất giữ các hạt giống bé thu thập được.")
            print("   - Tự động sắp xếp: Hạt giống trong kho luôn ngăn nắp theo thứ tự tăng dần.")
            # --- ĐOẠN 4: MỤC TIÊU & LỜI KHUYÊN (4 DÒNG) ---
            print("\n[4. MỤC TIÊU TRÒ CHƠI]")
            print("   - Bảo vệ HP: Giữ năng lượng cho Thỏ không bị về 0 để tiếp tục cuộc chơi.")
            print("   - Sưu tầm hạt giống: Tích lũy càng nhiều hạt giống giá trị cao càng tốt.")
            print("   - Rèn luyện trí tuệ: Chúc bé tính nhẩm ngày càng nhanh và chính xác!")

        elif choice == "5":     #Bé muốn nghỉ chơi
            self.hp = 0         #Đặt HP = 0 để kết thúc game

if __name__ == "__main__":
    game = BunnyGame()  #Tạo đối tượng game
    while game.hp > 0:  #Vòng lặp khi thỏ còn năng lượng
        game.play()     #Chạy từng lượt chơi
    print("\n Game kết thúc! Cảm ơn bé đã giúp đỡ Nông Trại Thỏ Ngọc!")








