import asyncio

from flask import Flask, Response, jsonify, render_template, request

from wiki.wiki import search_wiki

app = Flask(__name__)

# In-memory data to simulate CRUD operations
items = []


# Async function for event streaming
async def event_stream():
    while True:
        # Simulate a CRUD operation (getting items)
        items_data = await get_items()  # Simulate async CRUD operation
        message = f"data: {items_data}\n\n"
        yield message
        await asyncio.sleep(1)  # Non-blocking sleep to simulate time passing


# Simulate a simple in-memory CRUD operation (get items)
async def get_items():
    # Simulate a delay (like a database query or API call)
    await asyncio.sleep(1)
    return items  # Return the list of items (in-memory)


@app.route("/")
async def home():
    return render_template(
        "index.html",
        title="Hollywood Genealogy Project",
        header="Hollywood Genealogy Project",
    )


@app.route("/search", methods=["post"])
async def search():
    search_person = request.form.get("query")
    print(search_person)

    results = search_wiki(search_person)
    import pprint

    pprint.pprint(results)

    if results:
        page_title = results[0]["title"]
        page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        return jsonify({"status": "success", "url": page_url})

    return jsonify({"status": "error", "message": "No results found."})


# SSE route to stream data
@app.route("/events")
async def sse():
    # Flask needs to run the async generator in a thread-safe way
    def run_async_stream():
        loop = asyncio.new_event_loop()  # Create a new event loop
        asyncio.set_event_loop(loop)  # Set the event loop for the current thread
        return loop.run_until_complete(event_stream())  # Run the async generator

    return Response(run_async_stream(), content_type="text/event-stream")


# Route to trigger a "create" operation and simulate data updates
@app.route("/create_item", methods=["POST"])
async def create_item():
    new_item = "Sample Item"  # Simulated item (no real input for now)
    items.append(new_item)  # Simulate adding an item (in-memory CRUD)

    # After creation, return a response and stream updated data
    return jsonify(message="Item created, streaming data...")


if __name__ == "__main__":
    app.run(debug=True, threaded=True, load_dotenv=True)
