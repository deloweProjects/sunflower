let clickCount = 0;
const sun = document.getElementById("sun");
const main = document.getElementById("main");
const welcomeScreen = document.getElementById("welcomeScreen");
const countdownEl = document.getElementById("countdown");

sun.addEventListener("click", () => {
  clickCount++;

  if (clickCount === 3) {
    sun.classList.add("rotate");

    setTimeout(() => {
      main.classList.add("fadeOut");

      setTimeout(() => {
        welcomeScreen.classList.add("showWelcome");
        startCountdown();

        setTimeout(() => {
          countdownEl.classList.add("moveBottom");
        }, 4000);

      }, 1500);

    }, 3000);
  }
});

function startCountdown() {
  const targetDate = new Date("March 11, 2026 00:00:00").getTime();

  setInterval(() => {
    const now = new Date().getTime();
    const distance = targetDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((distance / (1000 * 60)) % 60);
    const seconds = Math.floor((distance / 1000) % 60);

    countdownEl.innerHTML =
      `${pad(days)}.${pad(hours)}.${pad(minutes)}.${pad(seconds)}`;

  }, 1000);
}

function pad(num) {
  return num < 10 ? "0" + num : num;
}
