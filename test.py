import unittest
import sqlite3
from app import app, load_data, save_data

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # SQLite 초기화
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

    def test_save_data_overwrites(self):
        # 데이터 저장 테스트: 중복 저장 시 덮어쓰기 확인
        save_data("작업 일보", "1", "직종", "관리")
        save_data("작업 일보", "1", "직종", "목수")
        data = load_data()
        self.assertEqual(data["작업 일보"]["1"]["직종"], "목수")
        # 중복 데이터 여부 확인
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM expenses WHERE tab = ? AND row = ? AND col = ?", 
                  ("작업 일보", "1", "직종"))
        count = c.fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)  # 단일 레코드만 존재해야 함

if __name__ == '__main__':
    unittest.main()