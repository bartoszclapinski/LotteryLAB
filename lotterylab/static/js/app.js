(function(){
  // ===== Chart Rendering =====
  function renderFrequencyChart(root){
    if(!root) return;
    const el = root.querySelector('#freq-chart');
    if(!el) return;
    let data;
    try{ data = JSON.parse(el.dataset.json || '{}'); }catch{ data = {}; }
    const expected = parseFloat(el.dataset.expected || '0');
    const x = Array.from({length: 49}, (_, i) => i + 1);
    const y = x.map(n => data[n] || 0);
    const trace = { x, y, type: 'bar', marker: {color: '#0066CC'}, name: 'Observed' };
    const traceExp = { x, y: x.map(()=> expected), type: 'scatter', mode: 'lines', line: {color:'#B25E00', dash:'dot'}, name: 'Expected' };
    const layout = { margin: {l:30,r:10,b:30,t:10}, height: 300, xaxis:{dtick:1}, yaxis:{title:'Count'}, legend:{orientation:'h'} };
    Plotly.newPlot(el, [trace, traceExp], layout, {displayModeBar:false});
  }

  // ===== Progress Bar & Navigation =====
  const topics = [
    '/partials/frequency',
    '/partials/randomness', 
    '/partials/generator',
    '/partials/patterns',
    '/partials/correlation',
    '/partials/trends'
  ];
  let currentIndex = 0;

  function updateProgress() {
    const fill = document.getElementById('progress-fill');
    const text = document.getElementById('current-topic');
    if (fill) fill.style.width = ((currentIndex + 1) / topics.length * 100) + '%';
    if (text) text.textContent = currentIndex + 1;
  }

  function navigateToTopic(index) {
    if (index < 0 || index >= topics.length) return;
    currentIndex = index;
    
    // Update sidebar active state
    const sidebarItems = document.querySelectorAll('.sidebar-item[hx-get]');
    sidebarItems.forEach((item, i) => {
      item.classList.toggle('active', i === index);
    });
    
    // Trigger HTMX request
    const mainContent = document.getElementById('main-content');
    if (mainContent && window.htmx) {
      htmx.ajax('GET', topics[index], {target: '#main-content', swap: 'innerHTML'});
    }
    
    updateProgress();
  }

  document.addEventListener('DOMContentLoaded', () => {
    renderFrequencyChart(document);
    updateProgress();
    
    // Prev/Next buttons
    const prevBtn = document.getElementById('prev-topic');
    const nextBtn = document.getElementById('next-topic');
    if (prevBtn) prevBtn.addEventListener('click', () => navigateToTopic(currentIndex - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => navigateToTopic(currentIndex + 1));
    
    // Sidebar item clicks
    const sidebarItems = document.querySelectorAll('.sidebar-item[hx-get]');
    sidebarItems.forEach((item, i) => {
      item.addEventListener('click', () => {
        currentIndex = i;
        // Update active state on all sidebar items
        sidebarItems.forEach((el, idx) => {
          el.classList.toggle('active', idx === i);
        });
        updateProgress();
      });
    });
  });

  document.body.addEventListener('htmx:afterSwap', (e) => {
    if(e && e.detail && e.detail.target && e.detail.target.id === 'frequency'){
      renderFrequencyChart(e.detail.target);
    }
    // Also check for main-content swaps
    if(e && e.detail && e.detail.target && e.detail.target.id === 'main-content'){
      renderFrequencyChart(e.detail.target);
    }
  });

  // ===== Monte Carlo Simulation =====
  function runMonteCarloSimulation(numSimulations) {
    const results = [];
    const NUMBERS = 49;
    const DRAWS_PER_SIM = 100;  // Simulate 100 draws per run
    const NUMBERS_PER_DRAW = 6;
    
    for (let sim = 0; sim < numSimulations; sim++) {
      // Generate random draws
      const frequencies = new Array(NUMBERS).fill(0);
      
      for (let draw = 0; draw < DRAWS_PER_SIM; draw++) {
        const selected = new Set();
        while (selected.size < NUMBERS_PER_DRAW) {
          selected.add(Math.floor(Math.random() * NUMBERS));
        }
        selected.forEach(n => frequencies[n]++);
      }
      
      // Calculate chi-square
      const totalObs = DRAWS_PER_SIM * NUMBERS_PER_DRAW;
      const expected = totalObs / NUMBERS;
      let chiSquare = 0;
      
      for (let i = 0; i < NUMBERS; i++) {
        chiSquare += Math.pow(frequencies[i] - expected, 2) / expected;
      }
      
      // Approximate p-value using chi-square distribution (df = 48)
      // Using simplified approximation for demo purposes
      const df = NUMBERS - 1;
      const pValue = 1 - chiSquareCDF(chiSquare, df);
      
      results.push({
        chiSquare,
        pValue,
        isRandom: pValue > 0.05
      });
    }
    
    // Calculate averages
    const avgChiSquare = results.reduce((a, b) => a + b.chiSquare, 0) / numSimulations;
    const avgPValue = results.reduce((a, b) => a + b.pValue, 0) / numSimulations;
    const randomPct = (results.filter(r => r.isRandom).length / numSimulations) * 100;
    
    return { avgChiSquare, avgPValue, randomPct };
  }
  
  // Simplified chi-square CDF approximation
  function chiSquareCDF(x, df) {
    if (x <= 0) return 0;
    // Use Wilson-Hilferty approximation
    const z = Math.pow(x / df, 1/3) - (1 - 2/(9*df));
    const denom = Math.sqrt(2/(9*df));
    const standardNormal = z / denom;
    // Standard normal CDF approximation
    return 0.5 * (1 + erf(standardNormal / Math.sqrt(2)));
  }
  
  // Error function approximation
  function erf(x) {
    const a1 =  0.254829592;
    const a2 = -0.284496736;
    const a3 =  1.421413741;
    const a4 = -1.453152027;
    const a5 =  1.061405429;
    const p  =  0.3275911;
    
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
  }

  // Monte Carlo UI handlers - initialize immediately since script has defer
  function initMonteCarlo() {
    const simSlider = document.getElementById('sim-slider');
    const simCount = document.getElementById('sim-count');
    const runBtn = document.getElementById('run-monte-carlo');
    
    if (simSlider && simCount) {
      simSlider.addEventListener('input', function() {
        simCount.textContent = parseInt(this.value).toLocaleString();
      });
    }
    
    if (runBtn) {
      runBtn.addEventListener('click', executeMonteCarloSimulation);
    }
  }
  
  function executeMonteCarloSimulation() {
    const simSlider = document.getElementById('sim-slider');
    const runBtn = document.getElementById('run-monte-carlo');
    const numSims = parseInt(simSlider?.value || 1000);
    
    if (runBtn) {
      runBtn.disabled = true;
      runBtn.textContent = '⏳ ...';
    }
    
    // Run simulation async to not block UI
    setTimeout(() => {
      try {
        const results = runMonteCarloSimulation(numSims);
        
        const chiEl = document.getElementById('mc-chi-square');
        const pEl = document.getElementById('mc-p-value');
        const pctEl = document.getElementById('mc-random-pct');
        
        if (chiEl) chiEl.textContent = results.avgChiSquare.toFixed(2);
        if (pEl) pEl.textContent = results.avgPValue.toFixed(4);
        if (pctEl) pctEl.textContent = results.randomPct.toFixed(1) + '%';
      } catch (err) {
        console.error('Monte Carlo error:', err);
        alert('Błąd symulacji: ' + err.message);
      }
      
      if (runBtn) {
        runBtn.disabled = false;
        runBtn.textContent = runBtn.dataset.label || 'Run Simulation';
      }
    }, 50);
  }
  
  // Expose globally for onclick fallback
  window.runMonteCarlo = executeMonteCarloSimulation;
  
  // Run on DOMContentLoaded OR immediately if DOM already loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMonteCarlo);
  } else {
    initMonteCarlo();
  }
})();
