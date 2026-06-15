const API_URL = "http://127.0.0.1:8000";

let radarChartInstance = null;

function updateSlider(el, valId, decimals) {
  document.getElementById(valId).textContent = parseFloat(el.value).toFixed(decimals);
}

const nameInput = document.getElementById('nameInput');
const launchBtn = document.getElementById('launchBtn');

nameInput.addEventListener('input', () => {
  launchBtn.disabled = nameInput.value.trim().length === 0;
});

launchBtn.addEventListener('click', () => {
  const name = nameInput.value.trim();
  if (!name) return;
  document.getElementById('welcomeText').textContent = `Welcome back, ${name}`;
  document.getElementById('screen1').classList.remove('active');
  setTimeout(() => {
    document.getElementById('screen2').classList.add('active');
  }, 50);
});

function logout() {
  document.getElementById('screen2').classList.remove('active');
  setTimeout(() => {
    document.getElementById('screen1').classList.add('active');
    document.getElementById('resultArea').style.display = 'none';
    document.getElementById('emptyState').style.display = 'flex';
    document.getElementById('aiResult').style.display = 'none';
    nameInput.value = '';
    launchBtn.disabled = true;
  }, 50);
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 4000);
}

function setLoading(on) {
  const btn = document.getElementById('inferBtn');
  const txt = document.getElementById('inferBtnText');
  const icon = document.getElementById('inferBtnIcon');
  const skel = document.getElementById('skeletonLoader');
  const res = document.getElementById('resultArea');
  const empty = document.getElementById('emptyState');

  if (on) {
    btn.disabled = true;
    txt.textContent = 'Running inference...';
    skel.style.display = 'block';
    res.style.display = 'none';
    empty.style.display = 'none';
  } else {
    btn.disabled = false;
    txt.textContent = 'Execute Inference';
    skel.style.display = 'none';
    res.style.display = 'block';
  }
}

function getPayload() {
  return {
    branch: document.getElementById('branch').value,
    college_tier: document.getElementById('college_tier').value,
    cgpa: parseFloat(document.getElementById('cgpa').value),
    backlogs: parseInt(document.getElementById('backlogs').value),
    coding_skills: parseInt(document.getElementById('coding_skills').value),
    dsa_score: parseFloat(document.getElementById('dsa_score').value),
    aptitude_score: parseFloat(document.getElementById('aptitude_score').value),
    communication_skills: parseFloat(document.getElementById('communication_skills').value),
    ml_knowledge: parseFloat(document.getElementById('ml_knowledge').value),
    system_design: parseFloat(document.getElementById('system_design').value),
    internships: parseInt(document.getElementById('internships').value),
    projects_count: parseInt(document.getElementById('projects_count').value),
    certifications: parseInt(document.getElementById('certifications').value),
    hackathons: parseInt(document.getElementById('hackathons').value),
    open_source_contributions: parseInt(document.getElementById('open_source_contributions').value),
    extracurriculars: parseInt(document.getElementById('extracurriculars').value)
  };
}

function buildRadarChart(payload) {
  const ctx = document.getElementById('radarChart').getContext('2d');
  if (radarChartInstance) radarChartInstance.destroy();
  radarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Coding', 'DSA', 'ML', 'System Design', 'Communication', 'Aptitude%'],
      datasets: [{
        label: 'Your Profile',
        data: [
          payload.coding_skills,
          payload.dsa_score,
          payload.ml_knowledge,
          payload.system_design,
          payload.communication_skills,
          payload.aptitude_score / 10
        ],
        backgroundColor: 'rgba(13,156,90,0.12)',
        borderColor: 'rgba(13,156,90,0.8)',
        pointBackgroundColor: '#0D9C5A',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#0D9C5A',
        borderWidth: 2
      }]
    },
    options: {
      animation: { duration: 800, easing: 'easeInOutQuart' },
      scales: {
        r: {
          min: 0, max: 10,
          grid: { color: 'rgba(255,255,255,0.06)' },
          angleLines: { color: 'rgba(255,255,255,0.06)' },
          pointLabels: { color: '#666680', font: { size: 11, family: 'Inter' } },
          ticks: { display: false }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15,15,35,0.95)',
          borderColor: 'rgba(123,114,240,0.3)',
          borderWidth: 1,
          titleColor: '#0D9C5A',
          bodyColor: '#C0C0D8',
          padding: 10
        }
      }
    }
  });
}

async function runInference() {
  const payload = getPayload();
  setLoading(true);

  try {
    const res = await fetch("/predict", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`API error ${res.status}`);
    const data = await res.json();
    setLoading(false);

    document.getElementById('placedResult').style.display = 'none';
    document.getElementById('notPlacedResult').style.display = 'none';
    document.getElementById('aiResult').style.display = 'none';

    if (data.status === 'Placed') {
      document.getElementById('kpiSalary').textContent = data.salary;
      document.getElementById('placedResult').style.display = 'block';
      buildRadarChart(payload);
    } else {
      const weakAreas = data.weak_areas || [];
      document.getElementById('kpiWeakCount').textContent = `${weakAreas.length} areas`;
      const container = document.getElementById('weakTags');
      container.innerHTML = weakAreas.map(a =>
        `<span class="weak-tag">↑ ${a.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}</span>`
      ).join('');
      document.getElementById('notPlacedResult').style.display = 'block';
      window._lastWeakAreas = weakAreas;
    }

  } catch (err) {
    setLoading(false);
    document.getElementById('emptyState').style.display = 'flex';
    document.getElementById('resultArea').style.display = 'none';
    showToast('Could not reach API. Make sure FastAPI is running on port 8000.');
  }
}

async function getAISuggestions() {
  const btn = document.getElementById('aiBtn');
  btn.disabled = true;
  btn.textContent = 'Generating suggestions...';

  try {
    const res = await fetch("/suggestions", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ weak_areas: window._lastWeakAreas || [] })
    });

    if (!res.ok) throw new Error('Suggestions API error');
    const data = await res.json();

    document.getElementById('aiText').textContent = data.suggestions;
    document.getElementById('aiResult').style.display = 'block';

  } catch (err) {
    showToast('AI suggestions unavailable. Check /suggestions endpoint.');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Get AI Improvement Suggestions`;
  }
}
