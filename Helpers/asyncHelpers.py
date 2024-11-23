import asyncio

def execute_multiple_calls(coros_or_futures):
    # Create an event loop to allow for parallel async calls
    loop = asyncio.new_event_loop()
    # Set our async event loop
    asyncio.set_event_loop(loop)
    # Gather our async calls into 
    group = asyncio.gather(coros_or_futures)
    # Run until all coroutines complete
    results = loop.run_until_complete(group)
    # Close our loop
    loop.close()
    # Return results
    return results