"""
/*********************************
Mã sinh viên: 202418977
Họ tên: Đào Quy Sang
*********************************/
"""

from typing import List, Optional


class Employee:
    """Lớp quản lý nhân sự thông thường."""

    def __init__(self, emp_id: str = "UNKNOWN", full_name: str = "Unnamed employee", base_salary: float = 0.0):
        if not emp_id or not emp_id.strip():
            raise ValueError("Mã nhân sự không được rỗng.")
        if not full_name or not full_name.strip():
            raise ValueError("Họ tên không được rỗng.")
        if base_salary < 0:
            raise ValueError("Lương cơ bản không được âm.")

        self._id = emp_id.strip()
        self._full_name = full_name.strip()
        self._base_salary = float(base_salary)

    @property
    def id(self) -> str:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def base_salary(self) -> float:
        return self._base_salary

    def increase_salary(self, value: float, by_percentage: bool = False) -> None:
        if value <= 0:
            raise ValueError("Giá trị tăng lương phải dương.")

        if by_percentage:
            self._base_salary += self._base_salary * (value / 100.0)
        else:
            self._base_salary += value

    def calculate_monthly_cost(self) -> float:
        return self._base_salary

    def display_info(self) -> None:
        print(f"[Employee] Mã: {self._id} | Họ tên: {self._full_name} | Lương CB: {self._base_salary:,.0f} VNĐ | Chi phí tháng: {self.calculate_monthly_cost():,.0f} VNĐ")

    def __del__(self):
        print(f"--> [Destructor Employee] Đối tượng {self._id} ({self._full_name}) bị giải phóng.")


class SoftwareEngineer(Employee):
    """Lớp Kỹ sư phần mềm kế thừa từ Employee."""

    def __init__(self, emp_id: str, full_name: str, primary_language: str, base_salary: float = 0.0, technical_allowance: float = 0.0):
        super().__init__(emp_id, full_name, base_salary)

        if not primary_language or not primary_language.strip():
            raise ValueError("Ngôn ngữ chính không được rỗng.")
        if technical_allowance < 0:
            raise ValueError("Phụ cấp kỹ thuật không được âm.")

        self._primary_language = primary_language.strip()
        self._technical_allowance = float(technical_allowance)

    @property
    def primary_language(self) -> str:
        return self._primary_language

    @property
    def technical_allowance(self) -> float:
        return self._technical_allowance

    def calculate_monthly_cost(self) -> float:
        return self._base_salary + self._technical_allowance

    def display_info(self) -> None:
        print(f"[SoftwareEngineer] Mã: {self._id} | Họ tên: {self._full_name} | Ngôn ngữ: {self._primary_language} | Lương CB: {self._base_salary:,.0f} VNĐ | Phụ cấp: {self._technical_allowance:,.0f} VNĐ | Chi phí tháng: {self.calculate_monthly_cost():,.0f} VNĐ")

    def __del__(self):
        print(f"--> [Destructor SoftwareEngineer] Đối tượng {self._id} ({self._full_name}) bị giải phóng.")


class ProjectTeam:
    """Lớp quản lý nhóm dự án."""

    def __init__(self, project_code: str, project_name: str, leader: Optional[Employee] = None):
        if not project_code or not project_code.strip():
            raise ValueError("Mã dự án không được rỗng.")
        if not project_name or not project_name.strip():
            raise ValueError("Tên dự án không được rỗng.")

        self._project_code = project_code.strip()
        self._project_name = project_name.strip()
        self._leader: Optional[Employee] = None
        self._members: List[Employee] = []

        if leader is not None:
            self.add_member(leader, make_leader=True)

    @property
    def project_code(self) -> str:
        return self._project_code

    @property
    def project_name(self) -> str:
        return self._project_name

    def contains(self, employee_id: str) -> bool:
        return any(emp.id == employee_id for emp in self._members)

    def add_member(self, employee: Employee, make_leader: bool = False) -> bool:
        if self.contains(employee.id):
            if make_leader:
                self._leader = employee
                print(f"[ProjectTeam] Nhân sự {employee.full_name} đã có trong nhóm -> Bổ nhiệm làm Trưởng nhóm mới thành công.")
                return True
            print(f"[ProjectTeam] LỖI: Nhân sự {employee.id} ({employee.full_name}) đã tồn tại trong nhóm!")
            return False

        self._members.append(employee)
        if make_leader:
            self._leader = employee
            print(f"[ProjectTeam] Đã thêm {employee.full_name} ({employee.id}) và bổ nhiệm làm TRƯỞNG NHÓM.")
        else:
            print(f"[ProjectTeam] Đã thêm thành công nhân sự {employee.full_name} ({employee.id}) vào nhóm.")

        return True

    def remove_member(self, employee_id: str) -> bool:
        if not self.contains(employee_id):
            print(f"[ProjectTeam] LỖI: Không tìm thấy nhân sự {employee_id} trong nhóm.")
            return False

        if self._leader and self._leader.id == employee_id:
            print(f"[ProjectTeam] TỪ CHỐI XÓA: Nhân sự {employee_id} đang là Trưởng nhóm! Phải chọn Trưởng nhóm thay thế trước.")
            return False

        self._members = [emp for emp in self._members if emp.id != employee_id]
        print(f"[ProjectTeam] Đã xóa thành công nhân sự {employee_id} khỏi nhóm.")
        return True

    def change_leader(self, new_leader: Employee) -> bool:
        if not self.contains(new_leader.id):
            self.add_member(new_leader, make_leader=True)
        else:
            self._leader = new_leader
            print(f"[ProjectTeam] Đã chuyển Trưởng nhóm sang {new_leader.full_name} ({new_leader.id}).")
        return True

    def calculate_total_monthly_cost(self) -> float:
        return sum(emp.calculate_monthly_cost() for emp in self._members)

    def display_team(self) -> None:
        print(f"\n================ NHÓM DỰ ÁN: [{self._project_code}] {self._project_name} ================")
        leader_str = f"{self._leader.full_name} ({self._leader.id})" if self._leader else "Chưa có"
        print(f"Trưởng nhóm: {leader_str}")
        print(f"Số lượng thành viên: {len(self._members)}")
        print("Danh sách thành viên (Gọi đa hình displayInfo()):")
        for idx, member in enumerate(self._members, 1):
            print(f"  {idx}. ", end="")
            member.display_info()
        print(f"--> TỔNG CHI PHÍ NGUỒN NHÂN LỰC/THÁNG: {self.calculate_total_monthly_cost():,.0f} VNĐ")
        print("=========================================================================\n")

    def __del__(self):
        print(f"--> [Destructor ProjectTeam] Giải phóng cấu trúc nhóm dự án {self._project_code}.")


# ==============================================================================
# KỊCH BẢN KIỂM THỬ 15 BƯỚC CÓ IN KẾT QUẢ HIỂN THỊ CHI TIẾT
# ==============================================================================
def main():
    print("================ KỊCH BẢN KIỂM THỬ THỰC TẾ ================\n")

    # 1. Tạo hai Employee bằng hai constructor khác nhau và in thông tin ra
    print("--- 1. Tạo 2 Employee bằng 2 Constructor khác nhau ---")
    emp1 = Employee("NV01", "Nguyen Van A")
    emp2 = Employee("NV02", "Tran Thi B", 10000000)
    emp1.display_info()
    emp2.display_info()

    # 2. Tạo hai Software Engineer bằng hai constructor khác nhau và in thông tin ra
    print("\n--- 2. Tạo 2 SoftwareEngineer bằng 2 Constructor khác nhau ---")
    se1 = SoftwareEngineer("SE01", "Le Van C", "Python")
    se2 = SoftwareEngineer("SE02", "Pham Van D", "C++", 15000000, 5000000)
    se1.display_info()
    se2.display_info()

    # 3. Tăng lương một nhân sự bằng số tiền cố định và in kết quả sau khi tăng
    print("\n--- 3. Tăng lương emp2 (NV02) thêm số tiền cố định +2,000,000 VNĐ ---")
    emp2.increase_salary(2000000)
    emp2.display_info()

    # 4. Tăng lương một nhân sự khác theo phần trăm và in kết quả sau khi tăng
    print("\n--- 4. Tăng lương se2 (SE02) theo tỷ lệ +10% ---")
    se2.increase_salary(10, by_percentage=True)
    se2.display_info()

    # 5. Tạo nhóm dự án không có trưởng nhóm và hiển thị thông tin nhóm ban đầu
    print("\n--- 5. Tạo nhóm dự án không có trưởng nhóm ---")
    team1 = ProjectTeam("PRJ01", "Hệ thống E-Commerce")
    team1.display_team()

    # 6. Thêm một nhân sự vào nhóm bằng addMember(employee)
    print("--- 6. Thêm nhân sự emp1 vào nhóm ---")
    team1.add_member(emp1)

    # 7. Thêm một kỹ sư bằng addMember(employee, True) để đặt làm trưởng nhóm
    print("\n--- 7. Thêm kỹ sư se2 vào nhóm và đặt làm TRƯỞNG NHÓM ---")
    team1.add_member(se2, make_leader=True)

    # 8. Thử thêm lại một thành viên đã tồn tại
    print("\n--- 8. Thử thêm lại nhân sự emp1 (đã có trong nhóm) ---")
    team1.add_member(emp1)

    # 9. Hiển thị danh sách bằng lời gọi đa hình
    print("\n--- 9. Hiển thị danh sách nhóm bằng lời gọi đa hình ---")
    team1.display_team()

    # 10. Tính tổng chi phí nhân sự hằng tháng
    print(f"--- 10. Tính tổng chi phí nhân sự hằng tháng của nhóm PRJ01: {team1.calculate_total_monthly_cost():,.0f} VNĐ ---")

    # 11. Thử xóa trưởng nhóm hiện tại và kiểm tra thao tác bị từ chối
    print("\n--- 11. Thử xóa Trưởng nhóm hiện tại (SE02) khi chưa có người thay thế ---")
    team1.remove_member("SE02")

    # 12. Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm
    print("\n--- 12. Đổi Trưởng nhóm sang se1, sau đó xóa SE02 khỏi nhóm ---")
    team1.change_leader(se1)
    team1.remove_member("SE02")
    team1.display_team()

    # 13. Tạo một nhóm thứ hai và thêm một nhân sự đã có ở nhóm thứ nhất
    print("--- 13. Tạo nhóm thứ 2 và thêm emp1 (nhân sự đã ở nhóm 1) ---")
    team2_ptr = ProjectTeam("PRJ02", "Ứng dụng Mobile", leader=emp2)
    team2_ptr.add_member(emp1)
    team2_ptr.display_team()

    # 14. Hủy nhóm thứ hai bằng cách xóa biến cục bộ
    print("--- 14. Hủy nhóm thứ hai (team2) ---")
    del team2_ptr

    # 15. Chứng minh nhân sự của nhóm thứ hai vẫn tồn tại sau khi nhóm bị hủy
    print("\n--- 15. Chứng minh nhân sự nhóm 2 (emp1, emp2) vẫn tồn tại bình thường ---")
    print("Kiểm tra sự tồn tại của emp1:")
    emp1.display_info()
    print("Kiểm tra sự tồn tại của emp2:")
    emp2.display_info()

    print("\n================ KẾT THÚC CHƯƠNG TRÌNH KIỂM THỬ ================")


if __name__ == "__main__":
    main()