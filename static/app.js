let currentQuote = null;
let guessesLeft = 4;

const quoteBox = document.getElementById("quoteBox");
const guessInput = document.getElementById("guessInput");
const guessBtn = document.getElementById("guessBtn");
const newBtn = document.getElementById("newBtn");
const hintBtn = document.getElementById("hintBtn");
const hintBox = document.getElementById("hintBox");

// Start a new round
newBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/get_quote");
    const data = await res.json();
    currentQuote = data;
    guessesLeft = data.guesses;

    // Show quote
    quoteBox.textContent = data.text;

    // Reset UI
    guessInput.value = "";
    hintBox.textContent = "";
    guessInput.disabled = false;
    guessBtn.disabled = false;
    hintBtn.disabled = false;
  } catch (err) {
    quoteBox.textContent = "⚠️ Could not load quote.";
  }
});

// Submit a guess
guessBtn.addEventListener("click", () => {
  if (!currentQuote) return;

  const guess = guessInput.value.trim();
  if (!guess) return;

  if (guess.toLowerCase() === currentQuote.author.toLowerCase()) {
    hintBox.textContent = `🎉 Correct! It was ${currentQuote.author}`;
    guessInput.disabled = true;
    guessBtn.disabled = true;
    hintBtn.disabled = true;
  } else {
    guessesLeft--;
    if (guessesLeft <= 0) {
      hintBox.textContent = `❌ Out of guesses! The answer was ${currentQuote.author}`;
      guessInput.disabled = true;
      guessBtn.disabled = true;
      hintBtn.disabled = true;
    } else {
      hintBox.textContent = `❌ Wrong! You have ${guessesLeft} guesses left.`;
    }
  }
});

// Get a hint
hintBtn.addEventListener("click", async () => {
  if (!currentQuote) return;

  try {
    const res = await fetch("/get_hint", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quote: currentQuote, guesses: guessesLeft })
    });
    const data = await res.json();
    if (data.hint) {
      hintBox.textContent = "💡 Hint: " + data.hint;
    }
  } catch (err) {
    hintBox.textContent = "⚠️ Could not fetch hint.";
  }
});

// Allow pressing Enter to submit guess
guessInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    guessBtn.click();
  }
});
