import asyncio


MAX_PARALLEL = 5


async def run_tests(test_list, username, access_key, cloud):
    running_tests = []
    num_tests_running = 0
    for i in test_list:
        if num_tests_running == MAX_PARALLEL:
            await running_tests.pop(0)
            num_tests_running -= 1
        task = asyncio.create_task(i(username, access_key, cloud))
        running_tests.append(task)
        num_tests_running += 1

    for i in running_tests:
        await i
