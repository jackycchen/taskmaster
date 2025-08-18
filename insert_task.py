import duckdb

conn = duckdb.connect('database.db')
conn.execute("INSERT INTO tasks (id, user_id, title, description, due_date, priority, status, notified) VALUES (2, 1, '测试提醒功能', '这是一个测试任务', '2025-08-16 18:15:50.545422', 2, 'pending', FALSE)")
conn.commit()
conn.close()
print('任务创建成功')