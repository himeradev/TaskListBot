import aiosqlite

async def init():
    async with aiosqlite.connect("tasks.db") as con:
        await con.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)"
        )
        await con.commit()

async def add_task(text):
    async with aiosqlite.connect("tasks.db") as con:
        await con.execute(
            "INSERT INTO tasks (task) VALUES (?)",
            (text,)
        )
        await con.commit()
        return True

async def remove_task(id):
    async with aiosqlite.connect("tasks.db") as con:
        await con.execute(
            "DELETE FROM tasks WHERE id = ?",
            (id,)
        )
        await con.commit()
        return True
        
async def get_tasks():
    async with aiosqlite.connect("tasks.db") as con:
        con.row_factory = aiosqlite.Row
        cur = await con.cursor()
        
        await cur.execute("SELECT * FROM tasks")
        rows = await cur.fetchall()
        
        if not rows:
            return False
        
        return [dict(row) for row in rows]
