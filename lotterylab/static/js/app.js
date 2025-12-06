(function(){
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

  document.addEventListener('DOMContentLoaded', () => {
    renderFrequencyChart(document);
  });

  document.body.addEventListener('htmx:afterSwap', (e) => {
    if(e && e.detail && e.detail.target && e.detail.target.id === 'frequency'){
      renderFrequencyChart(e.detail.target);
    }
  });
})();
