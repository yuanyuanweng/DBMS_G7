/* ========================================
   ワンちゃんの縁 — App Logic
   AI-Powered Stray Dog Adoption Platform
   ======================================== */

// ── Mock Dog Data ──────────────────────────────────────────────────────────
const DOGS_DATA = [
  {
    id: 1,
    name: "小豆 Komame",
    breed: "柴犬混種",
    age: "2歲",
    size: "小型",
    gender: "女生",
    city: "台北市",
    shelter: "台北市流浪動物之家",
    health: "已結紮、已施打疫苗",
    status: "待認養",
    urgent: false,
    tags: ["適合公寓", "性格溫和", "低度運動", "親近孩童"],
    story: "我叫小豆，是一隻喜歡在陽光下打盹的小傢伙。我不需要太大的空間，只需要每天一小段散步和一個讓我靠著的溫暖膝蓋。如果你也喜歡慢慢的生活，也許我們就是彼此的命定。",
    color: "#D9A57A",
    spotColor: "#C4714A",
  },
  {
    id: 2,
    name: "勇太 Yūta",
    breed: "米克斯（黑白花）",
    age: "4歲",
    size: "中型",
    gender: "男生",
    city: "新北市",
    shelter: "新北市動物保護處",
    health: "已結紮、健康活潑",
    status: "急需認養",
    urgent: true,
    tags: ["愛跑步", "需要院子", "單身/情侶適合", "聰明好訓練"],
    story: "我是勇太，一個充滿活力的大男孩。我最愛在公園裡奔跑，風吹過耳朵的感覺讓我覺得世界好大好美。希望找到一個喜歡戶外的家人，一起探索城市的每個角落！",
    color: "#5A5A5A",
    spotColor: "#FFFFFF",
  },
  {
    id: 3,
    name: "梅子 Umeko",
    breed: "比熊犬混種",
    age: "6個月",
    size: "小型",
    gender: "女生",
    city: "台中市",
    shelter: "台中市動物之家",
    health: "已施打第一劑疫苗",
    status: "待認養",
    urgent: false,
    tags: ["幼犬", "活潑好奇", "需要陪伴", "親人"],
    story: "我是梅子，才半歲的我什麼都好奇！每一個紙箱、每一片葉子、每一個新朋友，對我來說都是大冒險。如果你家有很多愛，我保證用我全部的軟萌回報給你！",
    color: "#F5E6C8",
    spotColor: "#D9A57A",
  },
  {
    id: 4,
    name: "次郎 Jirō",
    breed: "台灣犬",
    age: "5歲",
    size: "中型",
    gender: "男生",
    city: "台南市",
    shelter: "台南市動物保護處",
    health: "已結紮、已施打疫苗",
    status: "待認養",
    urgent: false,
    tags: ["穩重成熟", "適合有院子", "看家好手", "忠誠"],
    story: "大家都說台灣犬是最忠心的狗，我想說這是真的。我叫次郎，五年的歲月讓我更懂得珍惜每一個溫柔的撫摸。我不需要太多玩耍，只需要知道你在身邊。",
    color: "#8B6F52",
    spotColor: "#5C3D2E",
  },
  {
    id: 5,
    name: "雪見 Yukimi",
    breed: "薩摩耶混種",
    age: "3歲",
    size: "大型",
    gender: "女生",
    city: "台北市",
    shelter: "台北市流浪動物之家",
    health: "已結紮、已施打疫苗",
    status: "急需認養",
    urgent: true,
    tags: ["大型犬", "愛撒嬌", "需要空間", "友善其他狗"],
    story: "我是雪見，白色的毛讓我看起來像一朵雲。我很愛撒嬌，也很愛其他狗狗朋友。因為毛多，台灣夏天對我有點辛苦，希望找個有空調、有大空間的家——我會用最蓬鬆的擁抱回報你！",
    color: "#F0EDE8",
    spotColor: "#D4C9BD",
  },
  {
    id: 6,
    name: "橘子 Mikan",
    breed: "柯基混種",
    age: "1歲半",
    size: "小型",
    gender: "男生",
    city: "高雄市",
    shelter: "高雄市動物保護處",
    health: "已結紮、健康活潑",
    status: "待認養",
    urgent: false,
    tags: ["可愛短腿", "個性開朗", "適合家庭", "聰明"],
    story: "我叫橘子，因為毛色就像秋天的橘子！我的腿雖然短，但跑起來可不慢。我最愛玩接球遊戲，也喜歡和小孩玩耍。如果你家有笑聲，我就把快樂帶回去！",
    color: "#E8A84A",
    spotColor: "#C47A2A",
  },
];

let allDogs = [...DOGS_DATA];
let filteredDogs = [...DOGS_DATA];
let displayCount = 4;
let currentDog = null;
let likedDogs = new Set();

// ── Dog SVG Illustrations ───────────────────────────────────────────────────
function generateDogSVG(dog, size = 200) {
  const c = dog.color;
  const s = dog.spotColor;
  const isLight = isLightColor(c);
  const eyeColor = isLight ? "#2C2416" : "#FFFFFF";
  const noseColor = isLight ? "#4A3728" : "#2C2416";

  return `<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}">
    <rect width="200" height="200" fill="${dog.urgent ? '#FFF0EB' : '#F0E6D3'}"/>
    <ellipse cx="100" cy="185" rx="55" ry="10" fill="#D9C4A8" opacity="0.4"/>
    <!-- Tail -->
    <path d="M148 118 Q168 98 162 82 Q158 72 152 76 Q155 87 138 106Z" fill="${s}"/>
    <!-- Body -->
    <ellipse cx="108" cy="138" rx="48" ry="34" fill="${c}" stroke="${s}" stroke-width="0"/>
    <!-- Head -->
    <circle cx="70" cy="118" r="32" fill="${c}"/>
    <!-- Ears -->
    <ellipse cx="52" cy="94" rx="13" ry="19" fill="${s}" transform="rotate(-15 52 94)"/>
    <ellipse cx="88" cy="92" rx="11" ry="17" fill="${s}" transform="rotate(10 88 92)"/>
    <!-- Snout -->
    <ellipse cx="62" cy="128" rx="17" ry="12" fill="${isLight ? '#E8B98A' : '#8B6F52'}"/>
    <!-- Nose -->
    <ellipse cx="62" cy="122" rx="7" ry="5" fill="${noseColor}"/>
    <ellipse cx="60" cy="121" rx="2" ry="1.5" fill="white" opacity="0.5"/>
    <!-- Eyes -->
    <circle cx="56" cy="109" r="6" fill="white"/>
    <circle cx="57" cy="110" r="4" fill="${eyeColor === '#FFFFFF' ? '#2C2416' : '#2C2416'}"/>
    <circle cx="58" cy="108" r="1.5" fill="white"/>
    <circle cx="83" cy="107" r="6" fill="white"/>
    <circle cx="84" cy="108" r="4" fill="#2C2416"/>
    <circle cx="85" cy="106" r="1.5" fill="white"/>
    <!-- Mouth & Tongue -->
    <path d="M57 132 Q62 136 67 132" stroke="#8B6F52" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <ellipse cx="62" cy="136" rx="5" ry="4" fill="#E07070"/>
    <!-- Front legs -->
    <rect x="84" y="162" width="13" height="24" rx="6.5" fill="${c}"/>
    <rect x="103" y="162" width="13" height="24" rx="6.5" fill="${c}"/>
    <!-- Spot decoration -->
    <circle cx="118" cy="132" r="6" fill="${s}" opacity="0.35"/>
    <!-- Decorations -->
    <text x="148" y="82" font-size="12" fill="#C4714A" opacity="0.55">♥</text>
    <text x="28" y="82" font-size="10" fill="#8A9E8C" opacity="0.5">✿</text>
    ${dog.urgent ? '<text x="150" y="165" font-size="11" opacity="0.6">⚡</text>' : '<text x="148" y="168" font-size="11" opacity="0.5">🌸</text>'}
  </svg>`;
}

function isLightColor(hex) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return (0.299 * r + 0.587 * g + 0.114 * b) > 150;
}

// ── Render Dogs Grid ────────────────────────────────────────────────────────
function renderDogs(dogs, count) {
  const grid = document.getElementById('dogsGrid');
  grid.innerHTML = '';
  const subset = dogs.slice(0, count);

  if (subset.length === 0) {
    grid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:4rem 0;color:var(--brown);">
        <div style="font-size:3rem;margin-bottom:1rem;">🐾</div>
        <p style="font-family:var(--font-serif);font-size:1.1rem;">找不到符合條件的狗狗</p>
        <p style="font-size:0.85rem;margin-top:0.5rem;color:var(--gray);">試試調整篩選條件，或使用 AI 媒合</p>
      </div>`;
    return;
  }

  subset.forEach((dog, i) => {
    const card = document.createElement('div');
    card.className = 'dog-card';
    card.style.animationDelay = `${i * 0.07}s`;
    card.style.animation = 'fadeUp 0.5s ease both';

    const liked = likedDogs.has(dog.id);

    card.innerHTML = `
      <div class="dog-card-img">
        <div class="dog-card-img-placeholder">${generateDogSVG(dog, 160)}</div>
        <span class="dog-status-badge ${dog.urgent ? 'urgent' : ''}">${dog.status}</span>
      </div>
      <div class="dog-card-body">
        <p class="dog-card-name">${dog.name}</p>
        <p class="dog-card-meta">${dog.breed} · ${dog.age} · ${dog.gender} · ${dog.city}</p>
        <div class="dog-tags">
          ${dog.tags.slice(0, 3).map(t => `<span class="dog-tag">${t}</span>`).join('')}
        </div>
        <p class="dog-story">${dog.story}</p>
        <div class="dog-card-footer">
          <button class="adopt-btn" data-id="${dog.id}">認養我 🐾</button>
          <button class="heart-btn ${liked ? 'liked' : ''}" data-heart="${dog.id}">
            ${liked ? '❤️' : '🤍'}
          </button>
        </div>
      </div>`;

    card.querySelector('.adopt-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      openDogModal(dog);
    });

    card.querySelector('.heart-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      toggleLike(dog.id, e.currentTarget);
    });

    card.addEventListener('click', () => openDogModal(dog));
    grid.appendChild(card);
  });

  const loadBtn = document.getElementById('loadMoreBtn');
  loadBtn.style.display = dogs.length > count ? 'inline-flex' : 'none';
}

function toggleLike(id, btn) {
  if (likedDogs.has(id)) {
    likedDogs.delete(id);
    btn.textContent = '🤍';
    btn.classList.remove('liked');
    showToast('💔', '已取消收藏');
  } else {
    likedDogs.add(id);
    btn.textContent = '❤️';
    btn.classList.add('liked');
    showToast('❤️', '已加入收藏！');
  }
}

// ── Dog Modal ────────────────────────────────────────────────────────────────
function openDogModal(dog) {
  currentDog = dog;
  document.getElementById('modalDogName').textContent = dog.name;

  const hero = document.getElementById('modalDogHero');
  hero.innerHTML = generateDogSVG(dog, 280);
  hero.querySelector('svg').style.cssText = 'width:100%;height:auto;border-radius:12px;';

  const infoGrid = document.getElementById('modalInfoGrid');
  infoGrid.innerHTML = [
    ['品種', dog.breed],
    ['年齡', dog.age],
    ['性別', dog.gender],
    ['體型', dog.size],
    ['所在地', dog.city],
    ['健康狀態', dog.health],
    ['收容所', dog.shelter],
    ['認養狀態', dog.status],
  ].map(([l, v]) => `
    <div class="info-item">
      <div class="info-label">${l}</div>
      <div class="info-value">${v}</div>
    </div>`).join('');

  const storyBlock = document.getElementById('modalStoryBlock');
  const storyText = document.getElementById('modalStoryText');

  if (dog.story) {
    storyText.textContent = dog.story;
    storyBlock.style.display = 'block';
  } else {
    storyBlock.style.display = 'none';
  }

  document.getElementById('dogModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeDogModal() {
  document.getElementById('dogModal').classList.remove('active');
  document.body.style.overflow = '';
}

// ── Apply Modal ──────────────────────────────────────────────────────────────
function openApplyModal() {
  if (!currentDog) return;
  document.getElementById('applyDogName').textContent = currentDog.name;
  closeDogModal();
  document.getElementById('applyModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeApplyModal() {
  document.getElementById('applyModal').classList.remove('active');
  document.body.style.overflow = '';
}

function submitApply() {
  const name = document.getElementById('applyFullName').value.trim();
  const phone = document.getElementById('applyPhone').value.trim();
  const email = document.getElementById('applyEmail').value.trim();
  const city = document.getElementById('applyCity').value;
  const houseType = document.getElementById('applyHouseType').value;
  const reason = document.getElementById('applyReason').value.trim();

  if (!name || !phone || !email || !city || !houseType || !reason) {
    showToast('⚠️', '請填寫所有必填欄位');
    return;
  }

  const btn = document.getElementById('submitApply');
  btn.textContent = '⏳ 送出中…';
  btn.disabled = true;

  setTimeout(() => {
    closeApplyModal();
    btn.textContent = '🐾 送出申請';
    btn.disabled = false;
    showToast('🎉', `申請成功！我們會盡快聯絡你`);
    // Clear form
    ['applyFullName','applyPhone','applyEmail','applyCity',
     'applyHouseType','applyPets','applyReason','applyLifestyle']
      .forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
  }, 1400);
}

// ── AI Story Generation ──────────────────────────────────────────────────────
async function generateAIStory(dog) {
  const btn = document.getElementById('generateAIStoryBtn');
  const storyBlock = document.getElementById('modalStoryBlock');
  const storyText = document.getElementById('modalStoryText');

  btn.textContent = '⏳ AI 正在撰寫…';
  btn.disabled = true;
  storyBlock.style.display = 'block';
  storyText.textContent = '';

  const prompt = `你是一個充滿溫情的寵物認養平台寫手。請為以下這隻流浪狗狗，以「第一人稱」的方式，寫一段溫暖、真誠、讓人想認養的故事（100~150字繁體中文）。

狗狗資訊：
- 名字：${dog.name}
- 品種：${dog.breed}
- 年齡：${dog.age}
- 性別：${dog.gender}
- 個性標籤：${dog.tags.join('、')}
- 所在地：${dog.city}

請只輸出故事本文，不要加標題或說明。`;

  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 300,
        messages: [{ role: "user", content: prompt }]
      })
    });

    const data = await res.json();
    const text = data.content?.find(b => b.type === 'text')?.text || '';

    if (text) {
      await typewriterEffect(storyText, text.trim());
      dog.story = text.trim();
    } else {
      storyText.textContent = dog.story || '（故事生成失敗，請稍後再試）';
    }
  } catch (err) {
    console.error(err);
    storyText.textContent = dog.story || '（網路錯誤，請稍後再試）';
  } finally {
    btn.textContent = '✨ 重新生成故事';
    btn.disabled = false;
  }
}

async function typewriterEffect(el, text, speed = 22) {
  el.textContent = '';
  for (let i = 0; i < text.length; i++) {
    el.textContent += text[i];
    await new Promise(r => setTimeout(r, speed));
  }
}

// ── AI Search / Matching ─────────────────────────────────────────────────────
async function doAIMatch() {
  const input = document.getElementById('aiSearchInput').value.trim();
  if (!input) {
    showToast('💬', '請先描述你的生活方式');
    return;
  }

  const btn = document.getElementById('aiSearchBtn');
  btn.textContent = '⏳ AI 分析中…';
  btn.disabled = true;

  const dogList = DOGS_DATA.map(d => `ID:${d.id} 名字:${d.name} 品種:${d.breed} 年齡:${d.age} 體型:${d.size} 個性:${d.tags.join('、')}`).join('\n');
  const prompt = `你是一個寵物認養媒合專家。根據以下使用者描述，從狗狗列表中推薦最適合的1~3隻，並說明推薦原因（繁體中文）。

使用者描述：${input}

狗狗列表：
${dogList}

請以 JSON 格式回覆，格式如下（只輸出 JSON，不要加說明）：
{"recommendations":[{"id":數字,"reason":"推薦原因（2~3句話）"}]}`;

  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 600,
        messages: [{ role: "user", content: prompt }]
      })
    });

    const data = await res.json();
    const rawText = data.content?.find(b => b.type === 'text')?.text || '{}';
    const clean = rawText.replace(/```json|```/g, '').trim();
    const parsed = JSON.parse(clean);

    renderAIResults(parsed.recommendations || [], input);
  } catch (err) {
    console.error(err);
    renderAIResults([], input, true);
  } finally {
    btn.textContent = '🤖 AI 媒合';
    btn.disabled = false;
  }
}

function renderAIResults(recs, query, error = false) {
  const content = document.getElementById('aiResultContent');

  if (error || recs.length === 0) {
    content.innerHTML = `
      <div style="text-align:center;padding:2rem;color:var(--brown);">
        <div style="font-size:2.5rem;margin-bottom:1rem;">🐾</div>
        <p>${error ? 'AI 媒合暫時無法使用，請稍後再試。' : '根據你的描述，暫時沒有找到完全匹配的狗狗，請調整描述後再試。'}</p>
      </div>`;
    document.getElementById('aiResultModal').classList.add('active');
    document.body.style.overflow = 'hidden';
    return;
  }

  const matchedDogs = recs.map(r => ({
    dog: DOGS_DATA.find(d => d.id === r.id),
    reason: r.reason
  })).filter(r => r.dog);

  content.innerHTML = `
    <p style="font-size:0.85rem;color:var(--brown);margin-bottom:1.5rem;padding:10px;background:var(--pale-yellow);border-radius:8px;">
      🤖 根據「<strong>${query}</strong>」，AI 為你推薦以下 ${matchedDogs.length} 隻狗狗：
    </p>
    ${matchedDogs.map(({ dog, reason }) => `
      <div style="display:flex;gap:1rem;padding:1rem;background:var(--cream);border-radius:12px;margin-bottom:1rem;cursor:pointer;transition:box-shadow 0.2s;"
           onclick="closeAIModal();openDogModal(DOGS_DATA.find(d=>d.id===${dog.id}))"
           onmouseover="this.style.boxShadow='0 4px 16px rgba(74,55,40,0.12)'"
           onmouseout="this.style.boxShadow='none'">
        <div style="flex-shrink:0;">${generateDogSVG(dog, 80)}</div>
        <div>
          <p style="font-family:var(--font-serif);font-weight:700;color:var(--dark-brown);margin-bottom:3px;">${dog.name}</p>
          <p style="font-size:0.75rem;color:var(--gray);margin-bottom:6px;">${dog.breed} · ${dog.age} · ${dog.city}</p>
          <p style="font-size:0.82rem;color:var(--brown);line-height:1.6;">${reason}</p>
        </div>
      </div>`).join('')}`;

  document.getElementById('aiResultModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeAIModal() {
  document.getElementById('aiResultModal').classList.remove('active');
  document.body.style.overflow = '';
}

// ── Filter / Search ──────────────────────────────────────────────────────────
function doSearch() {
  const name = document.getElementById('searchName').value.trim().toLowerCase();
  const size = document.getElementById('filterSize').value;
  const city = document.getElementById('filterCity').value;

  filteredDogs = DOGS_DATA.filter(dog => {
    const matchName = !name || dog.name.toLowerCase().includes(name) || dog.breed.toLowerCase().includes(name);
    const matchSize = !size || dog.size === size;
    const matchCity = !city || dog.city === city;
    return matchName && matchSize && matchCity;
  });

  displayCount = 4;
  renderDogs(filteredDogs, displayCount);

  document.getElementById('dogs').scrollIntoView({ behavior: 'smooth', block: 'start' });

  showToast('🔍', `找到 ${filteredDogs.length} 隻符合條件的狗狗`);
}

// ── Toast ────────────────────────────────────────────────────────────────────
let toastTimer;
function showToast(icon, msg) {
  const toast = document.getElementById('toast');
  document.getElementById('toastIcon').textContent = icon;
  document.getElementById('toastMsg').textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}

// ── Login Modal ──────────────────────────────────────────────────────────────
function openLoginModal() {
  document.getElementById('loginModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeLoginModal() {
  document.getElementById('loginModal').classList.remove('active');
  document.body.style.overflow = '';
}

// ── Demo story rotation ──────────────────────────────────────────────────────
const demoStories = [
  `「我叫小豆，是一隻喜歡在陽光下打盹的小傢伙。我不需要太大的空間，只需要每天一小段散步和一個讓我靠著的溫暖膝蓋。如果你也喜歡慢慢的生活，也許我們就是彼此的命定。」`,
  `「我是勇太，一個充滿活力的大男孩。我最愛在公園裡奔跑，風吹過耳朵的感覺讓我覺得世界好大好美。希望找到一個喜歡戶外的家人，一起探索每個角落！」`,
  `「大家都說台灣犬是最忠心的狗，我想說這是真的。我叫次郎，五年的歲月讓我更懂得珍惜每一個溫柔的撫摸。我不需要太多玩耍，只需要知道你在身邊。」`,
];

let storyIndex = 0;
function rotateDemoStory() {
  storyIndex = (storyIndex + 1) % demoStories.length;
  const el = document.getElementById('demoStoryText');
  if (!el) return;
  el.style.opacity = '0';
  setTimeout(() => {
    el.textContent = demoStories[storyIndex];
    el.style.opacity = '1';
  }, 400);
  el.style.transition = 'opacity 0.4s ease';
}

// ── Intersection Observer for card animations ────────────────────────────────
function setupScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(el => {
      if (el.isIntersecting) {
        el.target.style.animationPlayState = 'running';
        observer.unobserve(el.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.step-card, .dog-card').forEach(el => {
    el.style.animationPlayState = 'paused';
    observer.observe(el);
  });
}

// ── Admin Panel stub ─────────────────────────────────────────────────────────
function openAdminPanel() {
  showToast('🔐', '管理後台需要登入後存取');
  setTimeout(openLoginModal, 800);
}

// ── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Initial render
  renderDogs(filteredDogs, displayCount);
  setupScrollAnimations();

  // Rotate demo story every 5s
  setInterval(rotateDemoStory, 5000);

  // Load more
  document.getElementById('loadMoreBtn').addEventListener('click', () => {
    displayCount += 4;
    renderDogs(filteredDogs, displayCount);
  });

  // Search
  document.getElementById('doSearch').addEventListener('click', doSearch);
  document.getElementById('searchName').addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch();
  });

  // AI search
  document.getElementById('aiSearchBtn').addEventListener('click', doAIMatch);
  document.getElementById('aiSearchInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') doAIMatch();
  });

  // Dog modal
  document.getElementById('closeDogModal').addEventListener('click', closeDogModal);
  document.getElementById('dogModal').addEventListener('click', e => {
    if (e.target === document.getElementById('dogModal')) closeDogModal();
  });

  // Apply modal
  document.getElementById('openApplyForm').addEventListener('click', openApplyModal);
  document.getElementById('closeApplyModal').addEventListener('click', closeApplyModal);
  document.getElementById('cancelApply').addEventListener('click', closeApplyModal);
  document.getElementById('submitApply').addEventListener('click', submitApply);
  document.getElementById('applyModal').addEventListener('click', e => {
    if (e.target === document.getElementById('applyModal')) closeApplyModal();
  });

  // AI Story in modal
  document.getElementById('generateAIStoryBtn').addEventListener('click', () => {
    if (currentDog) generateAIStory(currentDog);
  });

  // AI result modal
  document.getElementById('closeAiModal').addEventListener('click', closeAIModal);
  document.getElementById('aiResultModal').addEventListener('click', e => {
    if (e.target === document.getElementById('aiResultModal')) closeAIModal();
  });

  // Login modal
  document.getElementById('openLoginModal').addEventListener('click', e => {
    e.preventDefault();
    openLoginModal();
  });
  document.getElementById('closeLoginModal').addEventListener('click', closeLoginModal);
  document.getElementById('loginModal').addEventListener('click', e => {
    if (e.target === document.getElementById('loginModal')) closeLoginModal();
  });
  document.getElementById('doLogin').addEventListener('click', () => {
    closeLoginModal();
    showToast('👋', '歡迎回來！登入成功');
  });
  document.getElementById('openAdminPanel').addEventListener('click', e => {
    e.preventDefault();
    openAdminPanel();
  });

  // ESC key to close modals
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeDogModal();
      closeApplyModal();
      closeLoginModal();
      closeAIModal();
    }
  });

  // Make openDogModal globally accessible (for AI result onclick)
  window.openDogModal = openDogModal;
  window.closeAIModal = closeAIModal;
});
