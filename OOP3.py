#***************************************************
# Mã số sinh viên: 20248977
# Họ tên:          Đào Quý Sang
#***************************************************
from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from enum import Enum


class DeviceStatus(Enum):
    ACTIVE = "Active"
    UNDER_MAINTENANCE = "UnderMaintenance"
    RETIRED = "Retired"


class INetworkable(ABC):
    @property
    @abstractmethod
    def ip_address(self): ...

    @property
    @abstractmethod
    def is_connected(self): ...

    @abstractmethod
    def connect(self, ip_address): ...

    @abstractmethod
    def disconnect(self): ...


class Device(ABC):
    OLD_YEARS = 5  # quá ngưỡng này thì tính là thiết bị cũ

    def __init__(self, device_id, name, year_of_use, price, status=DeviceStatus.ACTIVE):
        if not device_id or not device_id.strip():
            raise ValueError("Mã thiết bị không được rỗng")
        if price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0")
        if year_of_use > datetime.now().year:
            raise ValueError("Năm sử dụng lớn hơn năm hiện tại")
        self._device_id = device_id.strip()
        self.name = name
        self.year_of_use = year_of_use
        self.price = Decimal(price)
        self.status = status

    @property
    def device_id(self):  # chỉ đọc: gán lại sẽ báo AttributeError
        return self._device_id

    @property
    def years_in_service(self):
        return datetime.now().year - self.year_of_use

    @property
    def needs_maintenance(self):
        return self.status == DeviceStatus.UNDER_MAINTENANCE or self.years_in_service > self.OLD_YEARS

    @abstractmethod
    def annual_maintenance_cost(self): ...

    def __str__(self):
        return (f"{type(self).__name__:<14} {self.device_id:<5} {self.name:<24} {self.year_of_use} "
                f"{self.price:>12,.0f}đ {self.status.value:<16} bảo trì: {self.annual_maintenance_cost():>10,.0f}đ")


class NetworkMixin(INetworkable):
    """Cài đặt mạng dùng chung, tránh lặp code giữa Computer và NetworkPrinter."""
    _ip = None

    @property
    def ip_address(self):
        return self._ip

    @property
    def is_connected(self):
        return self._ip is not None

    def connect(self, ip_address):
        if not ip_address or not ip_address.strip():
            raise ValueError("Địa chỉ IP không được rỗng")
        if self.is_connected:
            raise RuntimeError(f"{self.device_id} đang kết nối ({self._ip}), hãy ngắt trước")
        self._ip = ip_address.strip()

    def disconnect(self):
        self._ip = None

    def __str__(self):
        return f"{super().__str__()} | ip: {self._ip or '-'}"


class Computer(NetworkMixin, Device):
    def __init__(self, device_id, name, year_of_use, price, ram_gb, cpu, has_gpu, status=DeviceStatus.ACTIVE):
        super().__init__(device_id, name, year_of_use, price, status)
        self.ram_gb, self.cpu, self.has_gpu = ram_gb, cpu, has_gpu

    def annual_maintenance_cost(self):
        rate = Decimal("0.05")
        if self.has_gpu:
            rate += Decimal("0.02")
        if self.years_in_service > self.OLD_YEARS:
            rate += Decimal("0.01")
        return self.price * rate


class Printer(Device):
    TYPES = ("laser", "phun")
    PAGE_LIMIT = 100_000

    # is_color: đề tính phụ phí máy in màu nhưng không có thuộc tính này
    def __init__(self, device_id, name, year_of_use, price, printer_type, pages, is_color=False,
                 status=DeviceStatus.ACTIVE):
        super().__init__(device_id, name, year_of_use, price, status)
        if printer_type not in self.TYPES:
            raise ValueError(f"Loại máy in phải thuộc {self.TYPES}")
        self.printer_type, self.pages, self.is_color = printer_type, pages, is_color

    def annual_maintenance_cost(self):
        cost = self.price * Decimal("0.04")
        if self.pages > self.PAGE_LIMIT:
            cost += 500_000
        if self.is_color:
            cost += 300_000
        return cost


class NetworkPrinter(NetworkMixin, Printer):
    pass


class Projector(Device):
    LAMP_LIMIT = 3000

    def __init__(self, device_id, name, year_of_use, price, lumens, lamp_hours, status=DeviceStatus.ACTIVE):
        super().__init__(device_id, name, year_of_use, price, status)
        self.lumens, self.lamp_hours = lumens, lamp_hours

    def annual_maintenance_cost(self):
        cost = self.price * Decimal("0.03")
        if self.lamp_hours > self.LAMP_LIMIT:
            cost += 1_500_000
        return cost


class LabRoom:
    def __init__(self, room_id, name, capacity):
        self.room_id, self.name, self.capacity = room_id, name, capacity
        self._devices = []

    def find_device(self, device_id):
        return next((d for d in self._devices if d.device_id == device_id), None)

    def add_device(self, device):
        if not isinstance(device, Device):
            raise TypeError("Chỉ nhận đối tượng Device")
        if self.find_device(device.device_id):
            raise ValueError(f"Mã {device.device_id} đã có trong phòng {self.name}")
        self._devices.append(device)

    def remove_device(self, device_id):
        device = self.find_device(device_id)
        if device:
            self._devices.remove(device)
        return device is not None

    def annual_maintenance_cost(self):
        return sum(d.annual_maintenance_cost() for d in self._devices)  # đa hình

    def devices_requiring_maintenance(self):
        return [d for d in self._devices if d.needs_maintenance]

    def print_devices(self):
        print(f"\nPhòng {self.name} ({self.room_id}), {len(self._devices)}/{self.capacity} thiết bị:")
        for d in self._devices:
            print(" ", d)


def try_run(label, func, *args):
    try:
        func(*args)
    except (ValueError, TypeError, RuntimeError) as e:
        print(f"{label}: {type(e).__name__} - {e}")


def main():
    c1 = Computer("C01", "Dell OptiPlex 7090", 2022, 20_000_000, 16, "Core i7", True)
    c2 = Computer("C02", "HP ProDesk 400", 2018, 15_000_000, 8, "Core i5", False, DeviceStatus.UNDER_MAINTENANCE)
    p1 = Printer("P01", "Canon LBP 2900", 2023, 4_000_000, "laser", 15_000)
    p2 = NetworkPrinter("P02", "HP LaserJet M404dn", 2021, 10_000_000, "laser", 120_000, True)
    pr = Projector("PR01", "Panasonic PT-LB426", 2019, 25_000_000, 4100, 3200)
    spare = Projector("PR02", "Epson EB-X06", 2024, 9_000_000, 3600, 200)  # chưa gán phòng

    lab1, lab2 = LabRoom("L101", "Lab 101", 40), LabRoom("L102", "Lab 102", 30)
    for d in (c1, c2, p2):
        lab1.add_device(d)
    for d in (p1, pr):
        lab2.add_device(d)

    print("== Thêm trùng mã / dữ liệu sai ==")
    try_run("Trùng mã", lab1.add_device, c1)
    try_run("Thiết bị None", lab1.add_device, None)
    try_run("Mã rỗng", Computer, " ", "X", 2020, 1, 8, "i3", False)
    try_run("Giá <= 0", Projector, "X", "X", 2020, 0, 1000, 0)
    try_run("Năm tương lai", Printer, "X", "X", 2099, 1, "laser", 0)
    try_run("Loại máy in", Printer, "X", "X", 2020, 1, "kim", 0)

    print("\n== Danh sách thiết bị ==")
    lab1.print_devices()
    lab2.print_devices()

    print("\n== Tổng chi phí bảo trì ==")
    for lab in (lab1, lab2):
        print(f"{lab.name}: {lab.annual_maintenance_cost():,.0f}đ")

    print("\n== Thiết bị cần bảo trì ==")
    for lab in (lab1, lab2):
        for d in lab.devices_requiring_maintenance():
            print(f"{lab.name}: {d.device_id} ({d.status.value}, {d.years_in_service} năm)")

    print("\n== Thiết bị mạng (duyệt qua INetworkable) ==")
    everything = [c1, c2, p1, p2, pr, spare]
    nets = [d for d in everything if isinstance(d, INetworkable)]
    for i, n in enumerate(nets, start=10):
        n.connect(f"192.168.1.{i}")
    try_run("Kết nối lại", nets[0].connect, "192.168.1.99")
    try_run("IP rỗng", nets[1].connect, "")
    for n in nets:
        print(f"{n.device_id}: connected={n.is_connected}, ip={n.ip_address}")
    nets[0].disconnect()
    print(f"Sau ngắt: {nets[0].device_id} connected={nets[0].is_connected}, ip={nets[0].ip_address}")


if __name__ == "__main__":
    main()