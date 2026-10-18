"use strict";

const form = document.querySelector("#download-form");
const urlInput = document.querySelector("#media-url");
const statusLine = document.querySelector("#status");
const pasteButton = document.querySelector("#paste-button");

pasteButton.addEventListener("click", async () => {
  if (!navigator.clipboard || !navigator.clipboard.readText) {
    statusLine.textContent = "Zwischenablage nicht verfügbar. Bitte füge den Link manuell ein.";
    return;
  }
  try {
    const text = (await navigator.clipboard.readText()).trim();
    if (!text) {
      statusLine.textContent = "Die Zwischenablage ist leer.";
      return;
    }
    urlInput.value = text;
    statusLine.textContent = "Link eingefügt. Bitte prüfe ihn vor dem Fortfahren.";
    urlInput.focus();
  } catch {
    statusLine.textContent = "Kein Zugriff auf die Zwischenablage. Bitte füge den Link manuell ein.";
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const raw = urlInput.value.trim();
  let parsed;
  try {
    parsed = new URL(raw);
  } catch {
    statusLine.textContent = "Bitte gib eine gültige Webadresse ein.";
    return;
  }

  if (!["http:", "https:"].includes(parsed.protocol)) {
    statusLine.textContent = "Nur HTTP- oder HTTPS-Links werden akzeptiert.";
    return;
  }

  if (!document.querySelector("#rights-confirm").checked) {
    statusLine.textContent = "Bitte bestätige zuerst, dass du zum Download berechtigt bist.";
    return;
  }

  const format = form.elements.format.value.toUpperCase();
  const scope = form.elements.scope.value === "playlist" ? "ganze Playlist" : "einzelner Titel";
  statusLine.textContent = `Auswahl geprüft: ${format}, ${scope}. Diese veröffentlichte Demo startet noch keinen Download. Dafür muss ein separat installierter lokaler Dienst für zulässige Quellen eingerichtet und abgesichert werden.`;
});
