document
  .querySelector("#search-button")
  .addEventListener("click", function (event) {
    event.preventDefault();
    // Get the search query from the input field
    const query = document.querySelector("#person").value.trim();
    console.log(query);

    if (query === "") {
      alert("Please enter a search term.");
      return;
    }

    // Send the search query to the server using Fetch API
    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `query=${encodeURIComponent(query)}`,
    })
      .then((response) => response.json())
      .then((data) => {
        // Get the messages container
        const messagesContainer = document.querySelector("#messages");

        // Handle the response from the server
        if (data.status === "success") {
          const listItem = document.createElement("li");
          const link = document.createElement("a");
          link.href = data.url;
          link.target = "_blank";
          link.textContent = `Click here to view the Wikipedia page for ${query}`;
          listItem.appendChild(link);
          messagesContainer.appendChild(listItem);
        } else {
          // messagesContainer.textContent = data.message; // Display error message if no results
          const message = document.createElement("li");
          message.textContent = `No results for ${query}`;
          messagesContainer.append(message);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
      });
  });
