"""
🔑 Python logging 常見 Handler
✅ 總結
開發測試：StreamHandler + FileHandler 就夠用。
正式專案：常搭配 RotatingFileHandler / TimedRotatingFileHandler，避免 log 爆掉。
監控通知：SMTPHandler (寄信)、HTTPHandler (送到 API)、SysLogHandler (Linux)。
高併發  ：QueueHandler + QueueListener。
"""

# 01.StreamHandler				用途：把 log 輸出到「串流」(stream)，通常是螢幕（sys.stdout 或 sys.stderr）。
import logging
logging.StreamHandler()  # 預設輸出到 console

# 02.FileHandler				用途：把 log 存到檔案。
logging.FileHandler("mylog.log", encoding="utf-8")

# 03.RotatingFileHandler		用途：寫入檔案，但檔案超過設定大小後會自動「輪替」，產生新的檔案，避免檔案過大。
from logging.handlers import RotatingFileHandler
RotatingFileHandler("mylog.log", maxBytes=1024*1024, backupCount=5) # 檔案到 1MB 會換新檔，最多保留 5 個舊檔

# 04.TimedRotatingFileHandler	用途：依照時間切割 log 檔（每天/每小時/每分鐘一個檔案）。
from logging.handlers import TimedRotatingFileHandler
TimedRotatingFileHandler("mylog.log", when="midnight", interval=1, backupCount=7) # 每天午夜切一個新檔，最多保留 7 天

# 05.SMTPHandler 				用途：發送 log 到 Email（常用於錯誤通知）。
from logging.handlers import SMTPHandler
SMTPHandler(
    mailhost=("smtp.gmail.com", 587),
    fromaddr="me@gmail.com",
    toaddrs=["admin@gmail.com"],
    subject="Error Log",
    credentials=("me@gmail.com", "password"),
    secure=()
)

# 06.HTTPHandler 				用途：把 log 傳送到 HTTP/HTTPS 伺服器（例如 API 收集 log）。
from logging.handlers import HTTPHandler
HTTPHandler("localhost:8000", "/log", method="POST")

# 07.SocketHandler				用途：透過 Socket / UDP 傳送 log 到遠端伺服器。常用於分散式系統，把 log 集中到 Log Server。
# 07.DatagramHandler
from logging.handlers import SocketHandler
handler = SocketHandler('localhost', 9000)  # 送到 9000 這個「門牌」

# 08.SysLogHandler				用途：傳送 log 到作業系統的 syslog（Linux 常用）。
from logging.handlers import SysLogHandler
SysLogHandler(address="/dev/log")

# 09.QueueHandler				用途：把 log 發送到 queue.Queue，方便在多執行緒或多處理序環境集中管理 log。常搭配 QueueListener 使用。
from logging.handlers import QueueHandler
import queue
handler = QueueHandler(queue.Queue())

# 10.MemoryHandler				用途：先把 log 存在記憶體 buffer，等到數量/條件達成後再批次輸出（可以減少 I/O 負擔）。
from logging.handlers import MemoryHandler
handler = MemoryHandler(capacity=10, target=some_other_handler)