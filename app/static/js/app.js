/* ========================================
   PICKPET— Static JS
   Works with Flask Jinja2 templates.
   Dogs data is injected per-page via:
     const DOGS_FROM_SERVER = {{ dogs_json | tojson | safe }};
   on dogs/list.html
   ======================================== */

// ── SVG Dog Illustration Generator ──────────────────────────────────────────
function generateDogSVG(dog, size = 200) {
  const c   = dog.color     || '#D9A57A';
  const s   = dog.spotColor || dog.spot_color || '#C4714A';
  const light = isLightColor(c);
  const eyeC  = '#2C2416';
  const noseC = light ? '#4A3728' : '#2C2416';
  const snoutC = light ? '#E8B98A' : '#8B6F52';

  return `<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}">
    <rect width="200" height="200" fill="${dog.urgent || dog.is_urgent ? '#FFF0EB' : '#F0E6D3'}"/>
    <ellipse cx="100" cy="185" rx="55" ry="10" fill="#D9C4A8" opacity="0.4"/>
    <path d="M148 118 Q168 98 162 82 Q158 72 152 76 Q155 87 138 106Z" fill="${s}"/>
    <ellipse cx="108" cy="138" rx="48" ry="34" fill="${c}"/>
    <circle cx="70" cy="118" r="32" fill="${c}"/>
    <ellipse cx="52" cy="94" rx="13" ry="19" fill="${s}" transform="rotate(-15 52 94)"/>
    <ellipse cx="88" cy="92" rx="11" ry="17" fill="${s}" transform="rotate(10 88 92)"/>
    <ellipse cx="62" cy="128" rx="17" ry="12" fill="${snoutC}"/>
    <ellipse cx="62" cy="122" rx="7" ry="5" fill="${noseC}"/>
    <ellipse cx="60" cy="121" rx="2" ry="1.5" fill="white" opacity="0.5"/>
    <circle cx="56" cy="109" r="6" fill="white"/>
    <circle cx="57" cy="110" r="4" fill="${eyeC}"/>
    <circle cx="58" cy="108" r="1.5" fill="white"/>
    <circle cx="83" cy="107" r="6" fill="white"/>
    <circle cx="84" cy="108" r="4" fill="${eyeC}"/>
    <circle cx="85" cy="106" r="1.5" fill="white"/>
    <path d="M57 132 Q62 136 67 132" stroke="#8B6F52" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <ellipse cx="62" cy="136" rx="5" ry="4" fill="#E07070"/>
    <rect x="84" y="162" width="13" height="24" rx="6.5" fill="${c}"/>
    <rect x="103" y="162" width="13" height="24" rx="6.5" fill="${c}"/>
    <circle cx="118" cy="132" r="6" fill="${s}" opacity="0.35"/>
    <text x="148" y="82" font-size="12" fill="#C4714A" opacity="0.55">♥</text>
    <text x="28" y="82" font-size="10" fill="#8A9E8C" opacity="0.5">✿</text>
    ${(dog.urgent || dog.is_urgent) ? '<text x="150" y="165" font-size="11" opacity="0.6">⚡</text>' : '<text x="148" y="168" font-size="11" opacity="0.5">🌸</text>'}
  </svg>`;
}

function isLightColor(hex) {
  try {
    const r = parseInt(hex.slice(1,3),16);
    const g = parseInt(hex.slice(3,5),16);
    const b = parseInt(hex.slice(5,7),16);
    return (0.299*r + 0.587*g + 0.114*b) > 150;
  } catch { return true; }
}

// ── Inject SVG placeholders (list page) ─────────────────────────────────────
function injectDogSVGs() {
  document.querySelectorAll('.dog-card-img-placeholder').forEach(el => {
    const dog = {
      color:     el.dataset.color || '#D9A57A',
      spotColor: el.dataset.spot  || '#C4714A',
      urgent:    el.dataset.urgent === 'true'
    };
    el.innerHTML = generateDogSVG(dog, 160);
    el.style.cssText = 'width:100%;height:100%;';
  });
}

// ── AI Smart Match (calls Flask /ai/match POST) ──────────────────────────────
async function doAIMatch() {
  const input = document.getElementById('aiSearchInput');
  if (!input || !input.value.trim()) {
    showToast('💬', 'Please describe your lifestyle first');
    return;
  }

  const btn = document.getElementById('aiSearchBtn');
  btn.textContent = '⏳ Analysing…';
  btn.disabled = true;

  try {
    const res = await fetch('/ai/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input.value.trim() })
    });

    const data = await res.json();
    renderAIResults(data.recommendations || [], input.value.trim(), !res.ok);
  } catch (err) {
    console.error(err);
    renderAIResults([], input.value.trim(), true);
  } finally {
    btn.textContent = '🤖 AI Match';
    btn.disabled = false;
  }
}

// ── Render AI results modal ──────────────────────────────────────────────────
function renderAIResults(recs, query, error = false) {
  const content = document.getElementById('aiResultContent');
  const modal   = document.getElementById('aiResultModal');
  if (!content || !modal) return;

  // Use server-injected dog list if available, else empty
  const dogs = (typeof DOGS_FROM_SERVER !== 'undefined') ? DOGS_FROM_SERVER : [];

  if (error || recs.length === 0) {
    content.innerHTML = `
      <div style="text-align:center;padding:2rem;color:var(--brown);">
        <div style="font-size:2.5rem;margin-bottom:1rem;">🐾</div>
        <p>${error ? 'AI matching is temporarily unavailable. Please try again later.' : 'No perfect match found for your description. Try rephrasing!'}</p>
      </div>`;
    openModal(modal);
    return;
  }

  const matched = recs.map(r => ({
    dog:    dogs.find(d => d.id === r.id),
    reason: r.reason
  })).filter(r => r.dog);

  content.innerHTML = `
    <p style="font-size:0.85rem;color:var(--brown);margin-bottom:1.5rem;padding:10px;
              background:var(--pale-yellow);border-radius:8px;">
      🤖 Based on <strong>"${escapeHtml(query)}"</strong>, AI recommends ${matched.length} dog(s) for you:
    </p>
    ${matched.map(({ dog, reason }) => `
      <a href="/find-a-dog/${dog.id}" style="display:flex;gap:1rem;padding:1rem;background:var(--cream);
         border-radius:12px;margin-bottom:1rem;text-decoration:none;transition:box-shadow 0.2s;
         border:1px solid var(--light-gray);"
         onmouseover="this.style.boxShadow='0 4px 16px rgba(74,55,40,0.12)'"
         onmouseout="this.style.boxShadow='none'">
        <div style="flex-shrink:0;">${generateDogSVG(dog, 80)}</div>
        <div>
          <p style="font-family:var(--font-serif);font-weight:700;color:var(--dark-brown);margin-bottom:3px;">${escapeHtml(dog.name)}</p>
          <p style="font-size:0.75rem;color:var(--gray);margin-bottom:6px;">${escapeHtml(dog.breed)} · ${escapeHtml(dog.age)} · ${escapeHtml(dog.city)}</p>
          <p style="font-size:0.82rem;color:var(--brown);line-height:1.6;">${escapeHtml(reason)}</p>
        </div>
      </a>`).join('')}`;

  openModal(modal);
}

// ── Typewriter effect ────────────────────────────────────────────────────────
async function typewriterEffect(el, text, speed = 22) {
  el.textContent = '';
  for (let i = 0; i < text.length; i++) {
    el.textContent += text[i];
    await new Promise(r => setTimeout(r, speed));
  }
}

// ── Modal helpers ────────────────────────────────────────────────────────────
function openModal(el) {
  el.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal(el) {
  el.classList.remove('active');
  document.body.style.overflow = '';
}

// ── Toast ────────────────────────────────────────────────────────────────────
let _toastTimer;
function showToast(icon, msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  document.getElementById('toastIcon').textContent = icon;
  document.getElementById('toastMsg').textContent = msg;
  toast.classList.add('show');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}

// ── Escape HTML ──────────────────────────────────────────────────────────────
function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

// ── Demo story rotation (list page hero) ────────────────────────────────────
const DEMO_STORIES = [
  `"My name is Komame, and I love napping in sunny spots. I don't need a big space — just a short daily walk and a warm lap to curl up on. If you enjoy a slow, peaceful life, maybe we're each other's destiny."`,
  `"I'm Yūta, a big boy full of energy! I love sprinting through parks and feeling the wind in my ears. I'm looking for a family that loves the outdoors — let's explore every corner of the city together!"`,
  `"They say Taiwan mixed-breeds are the most loyal dogs, and I agree. My name is Jirō, and five years of life have taught me to treasure every gentle touch. I don't need much play — just knowing you're near."`,
];
let _storyIdx = 0;

function rotateDemoStory() {
  _storyIdx = (_storyIdx + 1) % DEMO_STORIES.length;
  const el = document.getElementById('demoStoryText');
  if (!el) return;
  el.style.transition = 'opacity 0.4s ease';
  el.style.opacity = '0';
  setTimeout(() => {
    el.textContent = DEMO_STORIES[_storyIdx];
    el.style.opacity = '1';
  }, 400);
}

// ── Heart / like (optimistic UI, sends POST to /dogs/<id>/like) ──────────────
function setupHeartButtons() {
  document.querySelectorAll('.heart-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const dogId = btn.dataset.heart;
      const liked = btn.classList.contains('liked');

      // Optimistic update
      btn.classList.toggle('liked');
      btn.textContent = liked ? '🤍' : '❤️';

      try {
        await fetch(`/dogs/${dogId}/like`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        showToast(liked ? '💔' : '❤️', liked ? 'Removed from favourites' : 'Added to favourites!');
      } catch {
        // Revert on failure
        btn.classList.toggle('liked');
        btn.textContent = liked ? '❤️' : '🤍';
      }
    });
  });
}

// ── Scroll animation observer ────────────────────────────────────────────────
function setupScrollAnimations() {
  // Legacy: pause/resume animation-play-state for step/dog cards
  const playStateObserver = new IntersectionObserver((entries) => {
    entries.forEach(el => {
      if (el.isIntersecting) {
        el.target.style.animationPlayState = 'running';
        playStateObserver.unobserve(el.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.step-card, .dog-card').forEach(el => {
    el.style.animationPlayState = 'paused';
    playStateObserver.observe(el);
  });

  // Reveal: fade-up on scroll for section headers, feature points, stat cards, etc.
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  const revealSelectors = [
    '.section-header',
    '.feature-point',
    '.stat-card',
    '.hero-stat',
    '.admin-section-title',
    '.cg-panel',
  ];
  document.querySelectorAll(revealSelectors.join(',')).forEach((el, i) => {
    el.classList.add('reveal');
    // Stagger siblings in the same parent
    const siblings = Array.from(el.parentElement?.children || []);
    const idx = siblings.indexOf(el);
    if (idx > 0 && idx <= 4) el.classList.add(`reveal-delay-${idx}`);
    revealObserver.observe(el);
  });
}

// ── Navbar shadow on scroll ───────────────────────────────────────────────────
function setupNavScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 24);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load
}

// ── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  // Inject SVG placeholders
  injectDogSVGs();
  setupScrollAnimations();
  setupNavScroll();
  setupHeartButtons();

  // Demo story rotation (hero section)
  if (document.getElementById('demoStoryText')) {
    setInterval(rotateDemoStory, 5000);
  }

  // AI Match button
  const aiBtn = document.getElementById('aiSearchBtn');
  if (aiBtn) {
    aiBtn.addEventListener('click', doAIMatch);
    document.getElementById('aiSearchInput')?.addEventListener('keydown', e => {
      if (e.key === 'Enter') doAIMatch();
    });
  }

  // AI Result modal close
  const aiModal = document.getElementById('aiResultModal');
  if (aiModal) {
    document.getElementById('closeAiModal')?.addEventListener('click', () => closeModal(aiModal));
    aiModal.addEventListener('click', e => { if (e.target === aiModal) closeModal(aiModal); });
  }

  // ESC closes any open modal
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.modal-overlay.active').forEach(m => closeModal(m));
  });

  // Flash messages auto-dismiss
  document.querySelectorAll('.flash-msg').forEach(el => {
    setTimeout(() => el.style.opacity = '0', 4000);
  });
});
