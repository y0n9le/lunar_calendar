from icalendar import Calendar, Event
from datetime import datetime, timedelta
from lunardate import LunarDate

chinese_days = [
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
]

chinese_months = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]

# 创建日历
cal = Calendar()
cal.add('prodid', '-//Lunar Calendar//')
cal.add('version', '2.0')
cal.add('X-WR-CALNAME', "农历")
cal.add('X-WR-CALDESC', "中国传统历法")
cal.add('X-WR-TIMEZONE', "Asia/Shanghai")

for year in range(1900, 2101):  # 1900-2100年
    for month in range(1, 13):
        for leap in [False, True]:  # 处理闰月
            for day in range(1, 31):
                try:
                    solar_date = LunarDate(year, month, day, leap).toSolarDate()
                    
                    # 格式
                    if leap:
                        lunar_name = f"闰{chinese_months[month-1]}{chinese_days[day-1]}"
                    else:
                        lunar_name = f"{chinese_months[month-1]}{chinese_days[day-1]}"
                    
                    event_name = f"{lunar_name}"

                    # 创建活动
                    event = Event()
                    event.add('summary', event_name)  # 活动名称
                    event.add('dtstart', solar_date)  # 开始日期
                    event.add('dtend', solar_date + timedelta(days=1))  # 结束日期
                    cal.add_component(event)
                except ValueError:
                    continue  # 跳过不存在的日期

# 保存文件
name = "lunar_calendar.ics"
with open(name, 'wb') as f:
    f.write(cal.to_ical())

print(f"已生成：{name}")
