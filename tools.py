from langchain_core.tools import tool
FLIGHTS_DB= {
    ("Hà Nội","Đà Nẵng"): [{"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy" },
                           {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business" },
                           {"airline": "Vietjet Air", "departure": "08:00", "arrival": "09:50", "price": 890_000, "class": "economy" },
                           {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
                           ],
    ("Hà Nội","Phú Quốc"): [{"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy" },
                            {"airline": "Vietjet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy" },
                            {"airline": "Vietjet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy" },
                            ],
    ("Hà Nội","Hồ Chí Minh"): [{"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy" },
                                {"airline": "Vietjet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy" },
                                {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy" },
                                {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
                                ],
    ("Hồ Chí Minh","Đà Nẵng"): [{"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy" },
                                {"airline": "Vietjet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy" },
                                ],
    ("Hồ Chí Minh","Phú Quốc"): [
                                {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy" },
                                {"airline": "Vietjet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
                                ],

}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "star": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "star": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "star": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "star": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "star": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "star": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "star": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "star": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "star": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "star": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "star": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "star": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "star": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm chuyến bay từ origin đến destination"""
    key = (origin, destination)
    if key not in FLIGHTS_DB:
        return f"Xin lỗi, hiện tại chúng tôi không có thông tin chuyến bay từ {origin} đến {destination}."
    flights = FLIGHTS_DB[key]
    result = f"Dưới đây là các chuyến bay từ {origin} đến {destination}:\n"
    for flight in flights:
        result += f"- Hãng: {flight['airline']}, Khởi hành: {flight['departure']}, Đến nơi: {flight['arrival']}, Giá: {flight['price']:,} VND, Hạng: {flight['class']}\n"
    return result
    pass

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại city"""
    if city not in HOTELS_DB:
        return f"Xin lỗi, hiện tại chúng tôi không có thông tin khách sạn tại {city}."
    hotels = [hotel for hotel in HOTELS_DB[city] if hotel["price_per_night"] <= max_price_per_night]
    if not hotels:
        return f"Xin lỗi, không có khách sạn nào tại {city} có giá dưới {max_price_per_night:,} VND mỗi đêm."
    result = f"Dưới đây là các khách sạn tại {city} có giá dưới {max_price_per_night:,} VND mỗi đêm:\n"
    for hotel in hotels:
        result += f"- Tên: {hotel['name']}, Sao: {hotel['star']}, Giá: {hotel['price_per_night']:,} VND/đêm, Khu vực: {hotel['area']}, Đánh giá: {hotel['rating']}/5\n"
    return result
    pass

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả tất cả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    
    Trả về: bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    def format_currency(amount: int) -> str:
        """Format tiền tệ theo chuẩn Việt Nam: X.XXX.XXXđ"""
        return f"{amount:,}đ".replace(",", ".")
    
    try:
        expense_items = expenses.split(',')
        total_spent = 0
        result = "Bảng chi phí:\n"
        
        for item in expense_items:
            if ':' in item:
                item = item.strip()
                name, amount = item.split(':', 1)
                try:
                    amount = int(amount.strip())
                    total_spent += amount
                    result += f"- {name.strip()}: {format_currency(amount)}\n"
                except ValueError:
                    result += f"- {name.strip()}: Hãy nhập lại số tiền\n"
        
        result += "---\n"
        result += f"Tổng chi: {format_currency(total_spent)}\n"
        result += f"Ngân sách: {format_currency(total_budget)}\n"
        
        remaining = total_budget - total_spent
        if remaining >= 0:
            result += f"Còn lại: {format_currency(remaining)}\n"
        else:
            result += f"Vượt ngân sách: {format_currency(abs(remaining))} đồng! Cần điều chỉnh.\n"
        
        return result
    except Exception as e:
        return f"Lỗi khi tính toán: {str(e)}"
    pass        