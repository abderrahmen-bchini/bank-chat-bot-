/*
  Wifak Assistant (vanilla JS)
  - English-first UI
  - Optional language switch (EN/FR/AR)
  - Sends messages to POST /chat (JSON: { message, lang })
  - Shows typing indicator (minimum 800ms)
  - Formats bot response (bold + bullet lines)
*/

const historyEl = document.getElementById("chatHistory");
const inputEl = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const typingEl = document.getElementById("typingIndicator");
const langSelect = document.getElementById("langSelect");

let currentLang = "en";

const I18N = {
  en: {
    you: "You",
    send: "Send",
    placeholder: "Type a message... (e.g., VPN, leave request, KYC)",
    error: "Sorry - something went wrong.\n• Make sure the Flask server is running.\n• Details: **{detail}**",
    langLabel: "Language",
    langChanged: "Language set to **English**.",
    topics: {
      onboarding: {
        label: "Onboarding",
        prompt: "I am new. What is the onboarding checklist (badge, IT setup, orientation)?",
      },
      leave: {
        label: "Leave Policy",
        prompt: "How do I request annual leave? What about sick leave and absences?",
      },
      it: {
        label: "IT Support",
        prompt: "I have an issue with VPN, email, or password login. What should I do?",
      },
      payroll: {
        label: "Payroll",
        prompt: "Where can I find my payslip and what should I do if my salary transfer is delayed?",
      },
      compliance: {
        label: "Compliance & KYC",
        prompt: "Compliance/KYC refresher: AML, audit readiness, internal policy - best practices?",
      },
      credit: {
        label: "Credit & Financing",
        prompt: "Credit/financing: required documents, internal steps, and Murabaha overview.",
      },
      islamic: {
        label: "Islamic Finance",
        prompt: "Explain these terms: ijara, murabaha, wakala, sukuk.",
      },
    },
  },
  fr: {
    you: "Vous",
    send: "Envoyer",
    placeholder: "Écrivez un message… (ex: VPN, demande de congé, KYC)",
    error: "Désolé — une erreur est survenue.\n• Vérifiez que le serveur Flask est démarré.\n• Détail: **{detail}**",
    langLabel: "Langue",
    langChanged: "Langue définie sur **Français**.",
    topics: {
      onboarding: {
        label: "Onboarding",
        prompt: "Je suis nouveau. Quelle est la checklist onboarding (badge, IT setup, orientation) ?",
      },
      leave: {
        label: "Congés",
        prompt: "Comment demander un congé annuel ? Et pour maladie / absence ?",
      },
      it: {
        label: "Support IT",
        prompt: "J’ai un souci VPN, email ou mot de passe. Que faire ?",
      },
      payroll: {
        label: "Paie",
        prompt: "Où trouver mon bulletin de paie et que faire si le virement est en retard ?",
      },
      compliance: {
        label: "Compliance & KYC",
        prompt: "Rappel Compliance/KYC: AML, audit, policy — bonnes pratiques ?",
      },
      credit: {
        label: "Crédit",
        prompt: "Crédit/financement: documents, étapes internes, et aperçu Mourabaha.",
      },
      islamic: {
        label: "Finance islamique",
        prompt: "Explique: ijara, mourabaha, wakala, sukuk.",
      },
    },
  },
  ar: {
    you: "أنت",
    send: "إرسال",
    placeholder: "اكتب رسالة… (مثال: VPN، إجازة، KYC)",
    error: "عذرًا — حدث خطأ.\n• تأكد أن خادم Flask يعمل.\n• التفاصيل: **{detail}**",
    langLabel: "اللغة",
    langChanged: "تم ضبط اللغة على **العربية**.",
    topics: {
      onboarding: {
        label: "الاندماج الوظيفي",
        prompt: "أنا جديد. ما هي قائمة الاندماج (بطاقة الدخول، إعداد IT، التعريف)؟",
      },
      leave: {
        label: "الإجازات",
        prompt: "كيف أطلب إجازة سنوية؟ وماذا عن الإجازة المرضية؟",
      },
      it: {
        label: "دعم تقنية المعلومات",
        prompt: "لدي مشكلة في VPN أو البريد أو كلمة المرور. ماذا أفعل؟",
      },
      payroll: {
        label: "الرواتب",
        prompt: "أين أجد كشف الراتب؟ وماذا أفعل إذا تأخر التحويل؟",
      },
      compliance: {
        label: "الامتثال و KYC",
        prompt: "تذكير: AML، التدقيق، السياسات الداخلية — أفضل الممارسات؟",
      },
      credit: {
        label: "التمويل",
        prompt: "التمويل/القروض: المستندات والخطوات الداخلية ونبذة عن المرابحة.",
      },
      islamic: {
        label: "المالية الإسلامية",
        prompt: "اشرح: الإجارة، المرابحة، الوكالة، الصكوك.",
      },
    },
  },
};

function t() {
  return I18N[currentLang] || I18N.en;
}

function nowTime() {
  const d = new Date();
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatBotText(raw) {
  const safe = escapeHtml(raw || "");
  const lines = safe.split(/\r?\n/);

  // Bold: **text** -> <strong>text</strong>
  const bolded = (s) => s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  const parts = [];
  const listItems = [];

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed) continue;

    if (/^(•|-)\s+/.test(trimmed)) {
      listItems.push(bolded(trimmed.replace(/^(•|-)\s+/, "")));
      continue;
    }

    if (listItems.length) {
      parts.push(`<ul>${listItems.map((li) => `<li>${li}</li>`).join("")}</ul>`);
      listItems.length = 0;
    }

    parts.push(`<p>${bolded(trimmed)}</p>`);
  }

  if (listItems.length) {
    parts.push(`<ul>${listItems.map((li) => `<li>${li}</li>`).join("")}</ul>`);
  }

  return parts.join("");
}

function scrollToBottom() {
  historyEl.scrollTop = historyEl.scrollHeight;
}

function createMessageEl(role, htmlContent, timeLabel) {
  const wrap = document.createElement("div");
  wrap.className = `message ${role} new`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${role}`;
  avatar.textContent = role === "bot" ? "W" : "U";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.innerHTML = `<span class="name">${role === "bot" ? "Wifak Assistant" : escapeHtml(
    t().you
  )}</span><span class="time">${escapeHtml(timeLabel)}</span>`;

  const content = document.createElement("div");
  content.className = "content";
  content.innerHTML = htmlContent;

  bubble.appendChild(meta);
  bubble.appendChild(content);

  if (role === "user") {
    wrap.appendChild(bubble);
    wrap.appendChild(avatar);
  } else {
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
  }

  return wrap;
}

function addUserMessage(text) {
  const html = `<p>${escapeHtml(text)}</p>`;
  const el = createMessageEl("user", html, nowTime());
  historyEl.appendChild(el);
  scrollToBottom();
}

function addBotMessage(text) {
  const html = formatBotText(text);
  const el = createMessageEl("bot", html, nowTime());
  historyEl.appendChild(el);
  scrollToBottom();

  // Remove the shimmer class after it runs once
  window.setTimeout(() => el.classList.remove("new"), 1100);
}

function setTyping(visible) {
  typingEl.hidden = !visible;
  if (visible) scrollToBottom();
}

function applyLanguage(lang) {
  currentLang = I18N[lang] ? lang : "en";
  localStorage.setItem("wifak_lang", currentLang);

  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === "ar" ? "rtl" : "ltr";
  document.body.classList.toggle("rtl", currentLang === "ar");

  inputEl.placeholder = t().placeholder;
  sendBtn.textContent = t().send;

  // Update quick topic labels
  document.querySelectorAll(".topic-btn").forEach((btn) => {
    const key = btn.getAttribute("data-topic");
    const item = t().topics[key];
    if (item) btn.textContent = item.label;
  });
}

async function postChat(message) {
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, lang: currentLang }),
  });

  // If the session expired, the backend returns JSON 401.
  if (res.status === 401) {
    throw new Error("Session expired. Please sign in again.");
  }

  // If we got redirected to /login, fetch will usually return HTML (not JSON).
  const ct = (res.headers.get("content-type") || "").toLowerCase();
  if (!ct.includes("application/json")) {
    throw new Error("Not authenticated. Redirecting to login.");
  }

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

async function sendMessage(presetText) {
  const text = (presetText ?? inputEl.value).trim();
  if (!text) return;

  addUserMessage(text);
  inputEl.value = "";
  inputEl.focus();

  const start = Date.now();
  setTyping(true);

  try {
    const data = await postChat(text);

    // Enforce minimum typing indicator time (800ms)
    const elapsed = Date.now() - start;
    const remaining = Math.max(0, 800 - elapsed);
    await new Promise((r) => setTimeout(r, remaining));

    setTyping(false);
    addBotMessage(data.response || "(No response)");
  } catch (err) {
    const elapsed = Date.now() - start;
    const remaining = Math.max(0, 800 - elapsed);
    await new Promise((r) => setTimeout(r, remaining));

    setTyping(false);
    addBotMessage(
      t()
        .error.replace("{detail}", escapeHtml(String(err.message || err)))
        .toString()
    );
  }
}

// Ripple effect for the send button
function addRipple(e) {
  const btn = e.currentTarget;
  const rect = btn.getBoundingClientRect();

  const ripple = document.createElement("span");
  ripple.className = "ripple";

  const size = Math.max(rect.width, rect.height);
  ripple.style.width = ripple.style.height = `${size}px`;

  const x = e.clientX - rect.left - size / 2;
  const y = e.clientY - rect.top - size / 2;
  ripple.style.left = `${x}px`;
  ripple.style.top = `${y}px`;

  btn.appendChild(ripple);
  window.setTimeout(() => ripple.remove(), 600);
}

// Language selector
if (langSelect) {
  const saved = localStorage.getItem("wifak_lang") || "en";
  langSelect.value = I18N[saved] ? saved : "en";

  langSelect.addEventListener("change", () => {
    applyLanguage(langSelect.value);
    addBotMessage(t().langChanged);
  });

  applyLanguage(langSelect.value);
}

// Quick topics
// We use data-topic keys; JS picks language-specific prompts.
document.querySelectorAll(".topic-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const key = btn.getAttribute("data-topic");
    const item = t().topics[key];
    const prompt = item?.prompt || btn.textContent;
    sendMessage(prompt);
  });
});

sendBtn.addEventListener("click", (e) => {
  addRipple(e);
  sendMessage();
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

window.addEventListener("load", () => scrollToBottom());
