const historyEl = document.getElementById("chatHistory");
const inputEl = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
let typingEl = document.getElementById("typingIndicator");
const langSelect = document.getElementById("langSelect");

const chatListEl = document.getElementById("chatList");
const newChatBtn = document.getElementById("newChatBtn");
const welcomeContentEl = document.getElementById("welcomeContent");
const welcomeMessageEl = document.getElementById("welcomeMessage");

let currentLang = "en";
let firstReplyHandled = false;

let currentChatId = localStorage.getItem("wifak_chat_id") || null;

const I18N = {
  en: {
    you: "You",
    send: "Send",
    placeholder: "Type a message... (e.g., VPN, leave request, KYC)",
    error: "Sorry - something went wrong.\n• Details: **{detail}**",
    langChanged: "Language set to **English**.",
    suggestionsTitle: "Suggestions:",
    suggestions: "VPN access, leave policy, payroll/payslip, KYC/AML, onboarding checklist.",
    historyHint: "Your previous conversations are available in the left sidebar.",
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
    error: "Désolé — une erreur est survenue.\n• Détail: **{detail}**",
    langChanged: "Langue définie sur **Français**.",
    suggestionsTitle: "Suggestions :",
    suggestions: "Accès VPN, politique de congés, paie/bulletin, KYC/AML, checklist onboarding.",
    historyHint: "Vos conversations précédentes sont disponibles dans la barre latérale.",
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
    error: "عذرًا — حدث خطأ.\n• التفاصيل: **{detail}**",
    langChanged: "تم ضبط اللغة على **العربية**.",
    suggestionsTitle: "اقتراحات:",
    suggestions: "الدخول إلى VPN، سياسة الإجازات، الرواتب/كشف الراتب، KYC/AML، قائمة الاندماج الوظيفي.",
    historyHint: "ستجد محادثاتك السابقة في الشريط الجانبي.",
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

function setWelcomeVisible(visible) {
  if (!welcomeMessageEl) return;
  welcomeMessageEl.style.display = visible ? "" : "none";
}

function appendMessageEl(el) {
  if (typingEl && typingEl.parentNode) {
    historyEl.insertBefore(el, typingEl);
    return;
  }
  historyEl.appendChild(el);
}

function createMessageEl(role, htmlContent, timeLabel) {
  const wrap = document.createElement("div");
  wrap.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${role}`;
  avatar.textContent = role === "bot" ? "W" : "U";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  const meta = document.createElement("div");
  meta.className = "meta";
  meta.innerHTML = `<span class="name">${role === "bot" ? "Wifak Assistant" : escapeHtml(
    t().you,
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

function addUserMessage(text, timeLabel = nowTime()) {
  setWelcomeVisible(false);
  const html = `<p>${escapeHtml(text)}</p>`;
  appendMessageEl(createMessageEl("user", html, timeLabel));
  scrollToBottom();
}

function addBotMessage(text, timeLabel = nowTime()) {
  const html = formatBotText(text);
  appendMessageEl(createMessageEl("bot", html, timeLabel));
  scrollToBottom();
}

function setTyping(visible) {
  if (!typingEl || firstReplyHandled) return;
  typingEl.hidden = !visible;
  if (visible) {
    // Keep typing indicator at the bottom.
    historyEl.appendChild(typingEl);
    scrollToBottom();
  }
}

function removeTypingIndicatorAfterFirstReply() {
  firstReplyHandled = true;
  if (typingEl && typingEl.parentNode) {
    typingEl.parentNode.removeChild(typingEl);
  }
  typingEl = null;
}

function applyLanguage(lang) {
  currentLang = I18N[lang] ? lang : "en";
  localStorage.setItem("wifak_lang", currentLang);
  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === "ar" ? "rtl" : "ltr";
  document.body.classList.toggle("rtl", currentLang === "ar");
  inputEl.placeholder = t().placeholder;
  sendBtn.textContent = t().send;

  if (welcomeContentEl) {
    welcomeContentEl.innerHTML =
      `<p><strong>${escapeHtml(t().suggestionsTitle)}</strong> ${escapeHtml(t().suggestions)}</p>` +
      `<p class="muted">${escapeHtml(t().historyHint)}</p>`;
  }
}

async function postChat(message) {
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, lang: currentLang, chat_id: currentChatId }),
  });

  let data = {};
  try {
    data = await res.json();
  } catch (_e) {
    data = {};
  }

  return { ok: res.ok, status: res.status, data };
}

function setActiveChatId(chatId) {
  currentChatId = chatId || null;
  if (currentChatId) {
    localStorage.setItem("wifak_chat_id", currentChatId);
  } else {
    localStorage.removeItem("wifak_chat_id");
  }
}

function clearConversationMessages() {
  setTyping(false);
  document.querySelectorAll(".message").forEach((el) => {
    if (el.id === "welcomeMessage" || el.id === "typingIndicator") return;
    el.remove();
  });
  setWelcomeVisible(true);
}

function formatChatUpdated(tsSeconds) {
  const d = new Date((Number(tsSeconds) || 0) * 1000);
  if (!Number.isFinite(d.getTime()) || d.getTime() === 0) return "";
  const now = new Date();
  const sameDay = d.toDateString() === now.toDateString();
  return sameDay
    ? d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    : d.toLocaleDateString([], { year: "numeric", month: "short", day: "2-digit" });
}

async function apiListChats() {
  const res = await fetch("/api/chats", { headers: { "Accept": "application/json" } });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data.chats || [];
}

async function apiCreateChat() {
  const res = await fetch("/api/chats", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

async function apiGetChat(chatId) {
  const res = await fetch(`/api/chats/${encodeURIComponent(chatId)}`, {
    headers: { "Accept": "application/json" },
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

async function refreshChatList() {
  if (!chatListEl) return;
  try {
    const chats = await apiListChats();
    chatListEl.innerHTML = "";

    if (!chats.length) {
      const empty = document.createElement("div");
      empty.className = "chat-empty";
      empty.textContent = "No conversations yet.";
      chatListEl.appendChild(empty);
      return;
    }

    for (const c of chats) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `chat-item${c.id === currentChatId ? " active" : ""}`;
      btn.innerHTML =
        `<span class="chat-item-title">${escapeHtml(c.title || "Chat")}</span>` +
        `<div class="chat-item-time">${escapeHtml(formatChatUpdated(c.updated_at))}</div>`;
      btn.addEventListener("click", () => loadChat(String(c.id)));
      chatListEl.appendChild(btn);
    }
  } catch (_e) {
    // If API fails, don’t block the main chat UX.
    chatListEl.innerHTML = "";
  }
}

async function loadChat(chatId) {
  if (!chatId) return;
  try {
    const chat = await apiGetChat(chatId);
    setActiveChatId(chatId);
    clearConversationMessages();

    const msgs = Array.isArray(chat.messages) ? chat.messages : [];
    setWelcomeVisible(!msgs.length);
    for (const m of msgs) {
      const role = String(m.role || "");
      const txt = String(m.content || "");
      const time = new Date((Number(m.ts) || 0) * 1000).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      if (role === "user") addUserMessage(txt, time);
      else addBotMessage(txt, time);
    }

    await refreshChatList();
    scrollToBottom();
  } catch (_e) {
    // If chat not found, reset.
    setActiveChatId(null);
    clearConversationMessages();
    await refreshChatList();
  }
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
    const { ok, status, data } = await postChat(text);

    if (data && data.chat_id) {
      const newId = String(data.chat_id);
      if (newId && newId !== String(currentChatId || "")) {
        setActiveChatId(newId);
      }
    }

    const elapsed = Date.now() - start;
    await new Promise((resolve) => setTimeout(resolve, Math.max(0, 800 - elapsed)));
    setTyping(false);

    const replyText =
      data.response || (ok ? "(No response)" : `Server error (HTTP ${status}).`);
    addBotMessage(replyText);

    removeTypingIndicatorAfterFirstReply();
    await refreshChatList();
  } catch (err) {
    const elapsed = Date.now() - start;
    await new Promise((resolve) => setTimeout(resolve, Math.max(0, 800 - elapsed)));
    setTyping(false);
    addBotMessage(
      t()
        .error.replace("{detail}", escapeHtml(String(err.message || err)))
        .toString(),
    );
    removeTypingIndicatorAfterFirstReply();
  }
}

if (langSelect) {
  const saved = localStorage.getItem("wifak_lang") || "en";
  langSelect.value = I18N[saved] ? saved : "en";
  langSelect.addEventListener("change", () => {
    applyLanguage(langSelect.value);
    addBotMessage(t().langChanged);
  });
  applyLanguage(langSelect.value);
}


if (newChatBtn) {
  newChatBtn.addEventListener("click", async () => {
    try {
      const created = await apiCreateChat();
      const id = String(created.chat_id || created.id || "");
      setActiveChatId(id || null);
    } catch (_e) {
      setActiveChatId(null);
    }

    clearConversationMessages();
    await refreshChatList();
    inputEl.focus();
  });
}

sendBtn.addEventListener("click", () => sendMessage());
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

window.addEventListener("load", async () => {
  await refreshChatList();
  if (currentChatId) await loadChat(currentChatId);
  scrollToBottom();
});
