import unittest
import sqlite3
from app import app, load_data, save_data, calculate_totals


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

    def test_save_data_overwrites(self):
        save_data("작업 일보", "직종", "관리")
        save_data("작업 일보", "직종", "목수")
        data = load_data()
        self.assertEqual(data["작업 일보"]["1"]["직종"], "목수")
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM expenses WHERE tab = ? AND row = ? AND col = ?", 
                  ("작업 일보", "1", "직종"))
        count = c.fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)

    def test_full_workflow(self):
        save_data("작업 일보",  "직종", "관리")
        save_data("작업 일보",  "전월 누계")
        save_data("작업 일보",  "금일 출역")
        data = load_data()
        self.assertEqual(data["작업 일보"]["1"]["직종"], "관리")
        data = calculate_totals(data)
        self.assertEqual(data["작업 일보"]["1"]["총 누계"], "15")
        response = self.client.get('/')
        self.assertNotIn(b"{% for", response.data)
        self.assertIn('data-row="21" data-col="소속팀"', response.data)

    def test_dashboard_summary(self):
        # 대시보드 테스트: 합계 표시 확인
        save_data("작업 일보", "1", "전월 누계", "10")
        save_data("작업 일보", "1", "금일 출역", "5")
        data = load_data()
        data = calculate_totals(data)
        response = self.client.get('/')
        self.assertIn('금일 출역 합계: ', response.data)
        self.assertIn('총 누계 합계: ', response.data)

if __name__ == '__main__':
    unittest.main()