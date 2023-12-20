import asyncio
import pytest
import aiohttp
import aiopg
import concurrent.futures

# 1. Тест для проверки разрешения promise с ожидаемым значением
@pytest.mark.asyncio
async def test_resolve_promise(event_loop):
    async def async_function():
        return "Expected Value"

    result = await async_function()
    assert result == "Expected Value"

# 2. Тест для проверки отклонения promise с ожидаемым исключением
@pytest.mark.asyncio
async def test_reject_promise(event_loop):
    async def async_function():
        raise ValueError("Expected Exception")

    with pytest.raises(ValueError, match="Expected Exception"):
        await async_function()

# 3. Тест для проверки корректного ответа при выполнении HTTP-запроса к внешнему API
@pytest.mark.asyncio
async def test_http_request(event_loop):
    async def fetch_data():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/todos/1") as response:
                return await response.json()

    result = await fetch_data()
    assert "userId" in result
    assert "id" in result
    assert "title" in result
    assert "completed" in result

# 4. Тест для проверки корректного добавления новой записи в базу данных
@pytest.mark.asyncio
async def test_database_interaction(event_loop):
    async def insert_into_database():
        connection = await aiopg.connect(database='test.db', loop=event_loop)
        async with connection.cursor() as cursor:
            await cursor.execute("INSERT INTO my_table (column1, column2) VALUES ('value1', 'value2')")
        connection.close()

    await insert_into_database()
 
# 5. Тест для проверки корректного возвращения результата при запуске асинхронной функции в отдельном потоке
@pytest.mark.asyncio
async def test_async_function_in_thread(event_loop):
    async def async_function():
        await asyncio.sleep(1)
        return "Expected Result"

    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(async_function())
        loop.close()
        return result

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await event_loop.run_in_executor(executor, run_in_thread)
    assert result == "Expected Result"
